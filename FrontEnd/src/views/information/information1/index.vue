<template>
	<div class="card">
		<h2 class="title">小区安防公告</h2>
		<el-table class="table-boarding" :data="tableData" border>
			<el-table-column prop="id" label="ID" width="180" />
			<el-table-column prop="title" label="标题">
				<template #default="{ row }">
					<a class="title-link" @click.stop.prevent="showAnnouncementDetails(row)">{{ row.title }}</a>
				</template>
			</el-table-column>
			<el-table-column prop="date" label="发布日期" />
			<el-table-column prop="author" label="发布人" />
			<el-table-column prop="status" label="状态" />
		</el-table>

		<el-dialog title="公告详情" :visible.sync="dialogVisible" :before-close="handleClose"
			custom-class="announcement-dialog">
			<div v-if="selectedAnnouncement">
				<h3>{{ selectedAnnouncement.title }}</h3>
				<p>{{ selectedAnnouncement.content }}</p>
			</div>
			<span slot="footer" class="dialog-footer">
				<el-button @click="dialogVisible = false">关闭</el-button>
			</span>
		</el-dialog>
	</div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
	setup() {
		const tableData = ref([]);
		const dialogVisible = ref(false);
		const selectedAnnouncement = ref(null);

		const showAnnouncementDetails = (announcement) => {
			selectedAnnouncement.value = announcement;
			dialogVisible.value = true;
		};

		const handleClose = (done) => {
			done();
		};

		const fetchAnnouncements = async () => {
			try {
				const response = await axios.get("http://localhost:5000/announce/receive_announcements");
				console.log(response);
				const data = response.data;
				tableData.value = data;
			} catch (error) {
				console.error(error);
			}
		};


		onMounted(fetchAnnouncements);

		return {
			tableData,
			dialogVisible,
			selectedAnnouncement,
			showAnnouncementDetails,
			handleClose,
		};
	},
};
</script>

  
<style scoped>
.card {
	width: 100%;
	padding: 20px;
}

.title {
	font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
	font-size: 30px;
	text-align: center;
	margin-bottom: 20px;
}

.table-boarding {
	width: 100%;
}

.title-link {
	color: inherit;
	cursor: pointer;
	text-decoration: none;
}

.title-link:hover {
	/* color: #409eff; */
	/* text-decoration: underline; */
}

.announcement-dialog {
	min-width: 400px;
}
</style>
  