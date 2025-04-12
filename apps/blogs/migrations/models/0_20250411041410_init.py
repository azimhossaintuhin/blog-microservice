from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `blogreader` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `blog_id` VARCHAR(255) NOT NULL,
    `user_id` VARCHAR(255) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `category` (
    `id` CHAR(36) NOT NULL PRIMARY KEY,
    `image` VARCHAR(255) NOT NULL DEFAULT '',
    `name` VARCHAR(255) NOT NULL DEFAULT '',
    `slug` VARCHAR(255) NOT NULL DEFAULT '',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `blog` (
    `id` CHAR(36) NOT NULL PRIMARY KEY,
    `image` VARCHAR(255) NOT NULL DEFAULT '',
    `author` VARCHAR(255) NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `slug` VARCHAR(255) NOT NULL,
    `content` LONGTEXT NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `category_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_blog_category_b53e6400` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `blog_blogreader` (
    `blog_id` CHAR(36) NOT NULL,
    `blogreader_id` INT NOT NULL,
    FOREIGN KEY (`blog_id`) REFERENCES `blog` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`blogreader_id`) REFERENCES `blogreader` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_blog_blogre_blog_id_9e372b` (`blog_id`, `blogreader_id`)
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
