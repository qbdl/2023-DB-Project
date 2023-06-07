<template>
	<div>
		<el-form label-position="left">
			<el-form-item label="标题">
				<el-input v-model="announcement.title" placeholder="请输入标题"></el-input>
			</el-form-item>
			<el-form-item label="发布人">
				<el-input v-model="announcement.author" placeholder="请输入发布人"></el-input>
			</el-form-item>
			<el-form-item label="公告内容">
				<WangEditor height="400px" v-model:value="announcement.content" />
			</el-form-item>
			<el-form-item>
				<el-button type="primary" @click="submitAnnouncement">发布公告</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>
  
<script lang="ts">
import { defineComponent, ref, defineEmit } from "vue";
import { ElMessage } from "element-plus";
import WangEditor from "@/components/WangEditor/index.vue";
import axios from "axios";

export default defineComponent({
	components: {
		WangEditor,
	},
	setup() {
		const announcement = ref({
			id: "",
			title: "",
			date: "",
			author: "",
			author_id: "1",//TODO: 要换成get当前用户的ID
			status: "已发布",
			content: "",
		});

		const submitAnnouncement = async () => {
			try {
				announcement.value.id = generateID();
				announcement.value.date = getCurrentDate();
				const response = await axios.post("http://localhost:5000/announce/create_announcement", announcement.value);
				console.log(response);
				// alert("公告发布成功");
				ElMessage({ message: "公告发布成功", type: "success" });
			} catch (error) {
				console.error(error);
				ElMessage({ message: "公告发布失败", type: "error" });
				// alert("公告发布失败");
			}
		};

		const generateID = () => {//TODO:修改为逐步增加
			return "00" + (Math.floor(Math.random() * 1000) + 1);
		};

		const getCurrentDate = () => {
			const currentDate = new Date();//TODO:改成当前时间
			return currentDate.toISOString().split("T")[0];
		};

		return {
			announcement,
			submitAnnouncement,
		};
	},
});
</script>
<style scoped lang="scss">
@import "./index.scss";
</style>
  