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
import { ref } from "vue";
export default {
	setup() {
		let tableData = [
  {
    id: "001",
    title: "关于增加小区门禁卡的通知",
    date: "2023-04-01",
    author: "物业管理部",
    status: "已发布",
    content: "为了提高小区的安全性，我们将会增加小区门禁卡的数量...",
  },
  {
    id: "002",
    title: "关于升级小区监控系统的通知",
    date: "2023-04-05",
    author: "物业管理部",
    status: "已发布",
    content: "为了提高小区安全管理水平，我们将对小区内的监控系统进行升级...",
  },
  {
    id: "003",
    title: "关于严禁闲杂人员进入小区的通知",
    date: "2023-04-10",
    author: "物业管理部",
    status: "已发布",
    content: "为了维护小区居民的生活安全，我们将严格执行门禁管理，严禁闲杂人员进入小区...",
  },
  {
    id: "004",
    title: "关于加强小区夜间巡逻安保的通知",
    date: "2023-04-15",
    author: "物业管理部",
    status: "已发布",
    content: "为了确保小区居民的安全，我们将在夜间加强巡逻安保工作，请各位居民注意安全...",
  },
  {
    id: "005",
    title: "关于防范入室盗窃的安全提示",
    date: "2023-04-20",
    author: "物业管理部",
    status: "已发布",
    content: "近期发生一些入室盗窃案件，请广大居民提高防范意识，加强门窗安全，外出时请确保房屋安全...",
  },
];


		const dialogVisible = ref(false);
		const selectedAnnouncement = ref(null);

		const showAnnouncementDetails = (announcement) => {
			selectedAnnouncement.value = announcement;
			dialogVisible.value = true;
		};

		const handleClose = (done) => {
			done();
		};

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
  