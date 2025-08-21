from typing import List

from sqlalchemy import delete, exists, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Follow, Media, Tweet
from src.database.repositories.user_repository import get_user_id_by
from src.handlers.exceptions import (
    IntegrityViolationException,
    PermissionException,
    RowNotFoundException,
)
from src.schemas.base_schemas import SuccessSchema
from src.schemas.like_schemas import LikeSchema
from src.schemas.tweet_schemas import (
    NewTweetResponseSchema,
    TweetBaseSchema,
    TweetResponseSchema,
    TweetSchema,
)
from src.schemas.user_schemas import UserSchema


async def collect_tweet_data(tweet: "Tweet") -> TweetSchema:


    attachments = [media.link for media in tweet.media]
    author_data = UserSchema.model_validate(tweet.author)
    likes_data = [LikeSchema.model_validate(like) for like in tweet.likes]

    return TweetSchema(
        id=tweet.id,
        content=tweet.tweet_data,
        attachments=attachments,
        author=author_data,
        likes=likes_data,
    )


async def is_tweet_exist(tweet_id: int, session: AsyncSession) -> bool:

    query = select(exists().where(Tweet.id == tweet_id))
    response = await session.scalar(query)
    return response is not None and response


async def get_tweets_selection(
    username: str, session: AsyncSession
) -> TweetResponseSchema:

    user_id = await get_user_id_by(username, session)
    if not user_id:
        raise RowNotFoundException()

    query = (
        select(Tweet)
        .join(Follow, Follow.following_id == Tweet.author_id)
        .where(Follow.follower_id == user_id)
    )
    tweets = (await session.scalars(query)).unique().all()

    tweet_schema = [await collect_tweet_data(tweet) for tweet in tweets]

    return TweetResponseSchema(tweets=tweet_schema)


async def add_tweet(
    username: str, tweet: TweetBaseSchema, session: AsyncSession
) -> NewTweetResponseSchema:

    user_id = await get_user_id_by(username, session)
    if not user_id:
        raise RowNotFoundException()

    new_tweet = Tweet(author_id=user_id, tweet_data=tweet.tweet_data)
    session.add(new_tweet)
    try:
        await save_tweet_and_update_media(new_tweet, tweet.tweet_media_ids, session)
    except IntegrityError as exc:
        await session.rollback()
        raise IntegrityViolationException(str(exc))
    return NewTweetResponseSchema(tweet_id=new_tweet.id)


async def save_tweet_and_update_media(
    tweet: Tweet, media_ids: List[int], session: AsyncSession
) -> None:

    await session.flush()
    if media_ids:
        query = update(Media).where(Media.id.in_(media_ids)).values(tweet_id=tweet.id)
        await session.execute(query)
    await session.commit()


async def delete_tweet(
    username: str, tweet_id: int, session: AsyncSession
) -> SuccessSchema:

    user_id = await get_user_id_by(username, session)
    if not user_id:
        raise RowNotFoundException()

    query = (
        delete(Tweet)
        .returning(Tweet.id)
        .where(Tweet.id == tweet_id, Tweet.author_id == user_id)
    )
    request = await session.execute(query)
    if not request.fetchone():
        raise PermissionException(
            f"User with {username=} can't delete tweet with {tweet_id=}"
        )

    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise IntegrityViolationException(str(exc))

    return SuccessSchema()
