from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `comment` (
    `id` CHAR(36) NOT NULL PRIMARY KEY,
    `blog_id` VARCHAR(255) NOT NULL,
    `user_id` VARCHAR(255) NOT NULL,
    `content` LONGTEXT NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `replay` (
    `id` CHAR(36) NOT NULL PRIMARY KEY,
    `user_id` VARCHAR(255) NOT NULL,
    `content` LONGTEXT NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `commet_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_replay_comment_f0d24c1d` FOREIGN KEY (`commet_id`) REFERENCES `comment` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `comment`;
        DROP TABLE IF EXISTS `replay`;"""
