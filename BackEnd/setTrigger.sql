
-- 暂不启用安防公告触发器，因为没有办法得到当前用户的ID --TODO:
-- Trigger for security_announcements
    -- notes : 插入security_announcements前检查author内容是否在personal_info中
-- DELIMITER //
-- CREATE TRIGGER security_announcements_before_insert
-- BEFORE INSERT ON security_announcements
-- FOR EACH ROW
-- BEGIN
--     DECLARE user_username VARCHAR(255);

--     SELECT username INTO user_username
--     FROM personal_info
--     WHERE id = NEW.author_id;

--     IF user_username IS NULL THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'Author does not exist in personal_info table.';
--     ELSEIF user_username != NEW.author THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'Author name does not match with personal_info table.';
--     END IF;
-- END //
-- DELIMITER ;


-- Trigger for personal_info
    -- notes : 插入personal_info表内容后 同步插入 users_outline
DELIMITER //
CREATE TRIGGER personal_info_after_insert
AFTER INSERT ON personal_info
FOR EACH ROW
BEGIN
    INSERT INTO users_outline(id, username, gender, idCard, email, address, createTime, status, avatar_path)
    VALUES (NEW.id, NEW.username, NEW.gender, NEW.idCard, NEW.email, NEW.address, NEW.createTime, 1, NEW.avatar_path);
END //
DELIMITER ;

    -- notes : 更新personal_info表内容后 同步更新 users_outline
DELIMITER //
CREATE TRIGGER personal_info_after_update
AFTER UPDATE ON personal_info
FOR EACH ROW
BEGIN
    UPDATE users_outline
    SET username = NEW.username, gender = NEW.gender, idCard = NEW.idCard, email = NEW.email, address = NEW.address, createTime = NEW.createTime, avatar_path = NEW.avatar_path
    WHERE id = OLD.id;
END //
DELIMITER ;

    -- notes : 删除personal_info表内容后 同步删除 users_outline
DELIMITER //
CREATE TRIGGER personal_info_after_delete
AFTER DELETE ON personal_info
FOR EACH ROW
BEGIN
    DELETE FROM users_outline
    WHERE id = OLD.id;
END //
DELIMITER ;

-- 暂时禁用，会导致两个触发器互相调用而报错
-- Trigger for users_outline
    -- notes : 更新users_outline表内容后同步 反向更新 personal_info
-- DELIMITER //
-- CREATE TRIGGER users_outline_after_update
-- AFTER UPDATE ON users_outline
-- FOR EACH ROW
-- BEGIN
--     UPDATE personal_info
--     SET username = NEW.username, gender = NEW.gender, idCard = NEW.idCard, email = NEW.email, address = NEW.address, createTime = NEW.createTime, avatar_path = NEW.avatar_path
--     WHERE id = OLD.id;
-- END //
-- DELIMITER ;

--     -- notes : 删除users_outline表内容后同步 反向删除 personal_info
-- DELIMITER //
-- CREATE TRIGGER users_outline_after_delete
-- AFTER DELETE ON users_outline
-- FOR EACH ROW
-- BEGIN
--     DELETE FROM personal_info
--     WHERE id = OLD.id;
-- END //
-- DELIMITER ;
