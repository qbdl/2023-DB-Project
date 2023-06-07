<template>
	<div class="card-container">
		<div class="card">
			<div class="header">
				<h2>个人信息</h2>
			</div>
			<div class="avatar-container">
				<!-- <el-avatar class="avatar" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" -->
				<el-avatar class="avatar" src="../../assets/images/userpic.jpg" :size="150" />
			</div>
			<!-- 描述性列表 -->
			<el-descriptions class="table_user" title="个人信息" direction="vertical" :column="2" size="large" border>
				<el-descriptions-item label="用户名" class="username-item">
					qbdl
				</el-descriptions-item>
				<el-descriptions-item label="电话">18105022730</el-descriptions-item>
				<el-descriptions-item label="地址" :span="2">
					苏州市吴中区吴中大道1188号
				</el-descriptions-item>
				<el-descriptions-item label="邮箱">likejie@tongji.edu.cn</el-descriptions-item>
				<el-descriptions-item label="小区名称">阳光花园</el-descriptions-item>
				<el-descriptions-item label="楼栋号">5栋</el-descriptions-item>
				<el-descriptions-item label="单元号">2单元</el-descriptions-item>
				<el-descriptions-item label="门牌号">502室</el-descriptions-item>
				<el-descriptions-item label="车位号">B-102</el-descriptions-item>
				<el-descriptions-item label="安防卡号">AF-123456</el-descriptions-item>
				<el-descriptions-item label="紧急联系人">张三</el-descriptions-item>
				<el-descriptions-item label="紧急联系电话">18212345678</el-descriptions-item>
			</el-descriptions>

		</div>
	</div>
</template>
  
<script lang="js">
import { ref } from "vue";

export default {
	name: "personalInfo",
	setup() {
		let size = ref("small");

		return {
			size,
		};
	},
};
</script>
  
<style scoped lang="scss">
.car-container {
	background-image: url("@/assets/images/background.png");
	/* background-image: url("@/assets/images/welcome_ori.png"); */
	z-index: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
	background-color: #f8f8f8;
	padding: 20px;
	border-radius: 15px;

	/* 新增属性 */
	background-size: cover;
	/* 缩放图片以完全覆盖容器，保持图片比例 */
	/* background-position: center; */
	/* 将图片居中显示 */
}

.card {
	background-color: rgba(255, 255, 255, 0.8);
	/* 设置背景颜色和透明度 */
	width: 100%;
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 20px;
	font-size: 1.2em;
	border-radius: 15px;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}


.header {
	width: 100%;
	text-align: center;
	margin-bottom: 20px;
}

.avatar-container {
	margin-bottom: 20px;
}

.table_user {
	width: 85%;
	margin-bottom: 20px;
}

.username-item {
	margin-bottom: 20px;
}

.action-btn {
	margin-bottom: 10px;
}
</style>
  