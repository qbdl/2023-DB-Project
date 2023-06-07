-- Inserting data into personal_info
INSERT INTO personal_info
(id, idCard, username, gender, phone, address, email, community_name, building_number, unit_number, door_number, parking_number, security_card_number, emergency_contact, emergency_contact_phone, avatar_path, faceInfo_path,password,createTime)
VALUES
    (1, '330622199001010001', '张三', '男', '13900139000', '上海市浦东新区XX路XX号', 'zhangsan@example.com', '绿地新城123', '3栋', '1单元', '301室', 'B-203', 'AF-234567', '李四', '18323456789', '../../assets/images/userpic.jpg', 'faceInfo1.txt','123',CURRENT_TIMESTAMP),
    (2, '330622199001010002', '李四', '女', '13900139001', '上海市浦东新区XX路XX号', 'lisi@example.com', '绿地新城123', '3栋', '1单元', '302室', 'B-203', 'AF-234568', '王五', '18323456790', '../../assets/images/userpic.jpg', 'faceInfo2.txt','123',CURRENT_TIMESTAMP),
    (3, '330622199001010003', '王五', '男', '13900139002', '上海市浦东新区XX路XX号', 'wangwu@example.com', '绿地新城123', '3栋', '1单元', '303室', 'B-203', 'AF-234569', '赵六', '18323456791', '../../assets/images/userpic.jpg', 'faceInfo3.txt','456',CURRENT_TIMESTAMP),
    (4, '330622199001010004', 'user', '男', '13900139003', '上海市浦东新区XX路XX号', 'user@example.com', '绿地新城123', '3栋', '1单元', '304室', 'B-203', 'AF-234570', '张三', '18323456792', '../../assets/images/userpic.jpg', 'faceInfo4.txt','123!',CURRENT_TIMESTAMP),
    (5, '330622199001010005', 'admin', '女', '13900139004', '上海市浦东新区XX路XX号', 'admin@example.com', '绿地新城123', '3栋', '1单元', '305室', 'B-203', 'AF-234571', '李四', '18323456793', '../../assets/images/userpic.jpg', 'faceInfo5.txt','123!',CURRENT_TIMESTAMP);

-- Inserting data into users_outline
-- INSERT INTO users_outline
-- (id, username, gender, idCard, email, address, createTime, status, avatar_path)
-- VALUES
--     (1, '张三', '男', '330622199001010001', 'zhangsan@example.com', '上海市浦东新区XX路XX号', CURRENT_TIMESTAMP, 1, '../../assets/images/userpic.jpg'),
--     (2, '李四', '女', '330622199001010002', 'lisi@example.com', '上海市浦东新区XX路XX号', CURRENT_TIMESTAMP, 1, '../../assets/images/userpic.jpg'),
--     (3, '王五', '男', '330622199001010003', 'wangwu@example.com', '上海市浦东新区XX路XX号', CURRENT_TIMESTAMP, 1, '../../assets/images/userpic.jpg'),
--     (4, 'user', '男', '330622199001010004', 'user@example.com', '上海市浦东新区XX路XX号', CURRENT_TIMESTAMP, 1, '../../assets/images/userpic.jpg'),
--     (5, 'admin', '女', '330622199001010005', 'admin@example.com', '上海市浦东新区XX路XX号', CURRENT_TIMESTAMP, 1, '../../assets/images/userpic.jpg');

-- Inserting data into security_announcements
INSERT INTO security_announcements
(id, title, date, author, author_id, status, content)
VALUES
    (1,'关于加强小区夜间巡逻安保的通知','2023-04-15','张三',1,'已发布', '为了确保小区居民的安全，我们将在夜间加强巡逻安保工作，请各位居民注意安全...'),
    (2,'关于防范入室盗窃的安全提示','2023-04-15','张三',1,'已发布', '近期发生一些入室盗窃案件，请广大居民提高防范意识，加强门窗安全，外出时请确保房屋安全...'),
    (3,'你五一出去玩了吗？','2023-04-15','张三',1,'已发布', '<pre><code >你五一出去玩了吗？</code></pre><p><br></p>'),
    (4, '关于增加小区门禁卡的通知', '2023-04-01', '张三', 1, '已发布', '为了提高小区的安全性，我们将会增加小区门禁卡的数量...'),
    (5, '关于升级小区监控系统的通知', '2023-04-05', '李四', 2, '已发布', '为了提高小区安全管理水平，我们将对小区内的监控系统进行升级...'),
    (6, '关于严禁闲杂人员进入小区的通知', '2023-04-10', '王五', 3, '已发布', '为了维护小区居民的生活安全，我们将严格执行门禁管理，严禁闲杂人员进入小区...');