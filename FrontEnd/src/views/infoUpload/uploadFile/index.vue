<template>
	<div class="out-div">
		<h1 class="header">文件上传</h1>
		<div class="main-container">
			<div class="upload-container">
				<el-upload :action="uploadUrl" :before-upload="beforeUpload" :on-success="onUploadSuccess"
					:on-error="onUploadError" :on-preview="handlePreview" :on-remove="handleRemove"
					:before-remove="beforeRemove" :file-list="fileList" list-type="text" :auto-upload="true"
					:multiple="true" :limit="3" :on-exceed="handleExceed">
					<div class="button-wrapper">
						<el-button size="large" type="primary">点击上传</el-button>
						<!-- 添加预览按钮 -->
						<!-- <el-button size="large" type="warning" @click="handlePreview(selectedFile)">预览文件</el-button> -->
						<div slot="tip" class="el-upload__tip" size="large">
							支持的文件类型：.xlsx, .xls, .csv, .doc, .docx, .pdf
						</div>
					</div>
				</el-upload>
			</div>
			<div class="preview-container">
				<file-preview :file="selectedFile"></file-preview>
			</div>
		</div>
	</div>
</template>
<script>
import { ref } from "vue";
import { ElMessage, ElMessageBox } from 'element-plus';
import FilePreview from "./FilePreview.vue";

export default {
	components: {
		FilePreview,
	},
	setup() {
		const selectedFile = ref(null); // 添加 selectedFile 数据属性
		const uploadUrl = "http://localhost:5000/upload/upload_file"; //上传API URL
		const fileList = ref([]);

		const beforeUpload = (file) => {
			const allowedExtensions = ["xlsx", "xls", "csv", "doc", "docx", "pdf"];
			const fileExtension = file.name.split(".").pop().toLowerCase();

			if (!allowedExtensions.includes(fileExtension)) {
				ElMessage.error("不支持的文件类型");
				return false;
			}
		};

		const onUploadSuccess = (response, file, fileList) => {
			ElMessage.success("文件上传成功");
		};

		const onUploadError = (error, file, fileList) => {
			ElMessage.error("文件上传失败");
		};

		const handlePreview = (file) => {
			selectedFile.value = file;
		};

		const handleRemove = (file, fileList) => {
			console.log("移除文件:", file);
		};

		const beforeRemove = (uploadFile, uploadFiles) => {
			return ElMessageBox.confirm(
				`取消传输 ${uploadFile.name} ?`
			).then(
				() => true,
				() => false
			);
		};

		const handleExceed = (files, uploadFiles) => {
			ElMessage.warning(
				`最多可选择3个文件，您本次选择了${files.length}个文件，总计${files.length + uploadFiles.length}个`
			);
		};

		return {
			uploadUrl,
			fileList,
			selectedFile,
			beforeUpload,
			onUploadSuccess,
			onUploadError,
			handlePreview,
			handleRemove,
			beforeRemove,
			handleExceed,
		};
	},
};
</script>


<style scoped>
.out-div {
	background-image: url("@/assets/images/background.png");
	z-index: 1;
	display: flex;
	flex-direction: column;
	background-color: #f8f8f8;
	padding: 20px;
	border-radius: 15px;

	background-size: cover;
}

.header {
	width: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
	margin-bottom: 20px;

}

.main-container {
	display: flex;
	flex-direction: row;
	gap: 20px;
	height: 65vh;
}

.upload-container {
	position: relative;
	/* 设置相对定位，以便子元素可以使用绝对定位 */
	flex: 1;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	align-items: center;
	/* background-color: #ffffff; */
	background-color: rgba(255, 255, 255, 0.8);
	padding: 20px;
	border-radius: 15px;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.button-wrapper {
	position: absolute;
	bottom: 20px;
	width: 100%;
	display: flex;
	flex-direction: column;
	align-items: center;
}

.el-upload__tip {
	text-align: center;
	margin-top: 20px;
}

.preview-container {
	flex: 1;
	display: flex;
	flex-direction: column;
	align-items: stretch;
	/* background-color: #ffffff; */
	background-color: rgba(255, 255, 255, 0.8);
	padding: 20px;
	border-radius: 15px;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>