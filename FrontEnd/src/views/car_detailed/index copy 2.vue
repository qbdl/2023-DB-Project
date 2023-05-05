<template>
	<div class="main-box">
		<div class="tree-filter">
			<el-tree :data="departmentData" node-key="id" default-expand-all :expand-on-click-node="false"
				:highlight-current="true" @current-change="handleDepartmentChange">
			</el-tree>
		</div>
		<div class="table-box">
			<div class="table-header">
				<el-input placeholder="请输入搜索内容" v-model="search" clearable @clear="handleSearch"
					@input="handleSearch"></el-input>
				<el-button type="primary" @click="handleAdd">新增用户</el-button>
			</div>
			<el-table :data="filteredData" border @sort-change="handleSortChange">
				<el-table-column type="index" label="序号" width="50"></el-table-column>
				<el-table-column prop="name" label="姓名" sortable></el-table-column>
				<el-table-column prop="age" label="年龄" sortable></el-table-column>
				<el-table-column prop="address" label="地址"></el-table-column>
				<el-table-column label="操作" width="180">
					<template #default="{ row }">
						<el-button size="mini" @click="handleEdit(row)">编辑</el-button>
						<el-button size="mini" @click="handleDelete(row)">删除</el-button>
					</template>
				</el-table-column>
			</el-table>
		</div>
	</div>
</template>
  
<script>
import axios from 'axios';

export default {
	data() {
		return {
			search: '',
			departmentData: [
				// 假设这是从 API 获取的部门数据
				{ id: 1, label: '部门1', children: [{ id: 4, label: '部门1-1' }] },
				{ id: 2, label: '部门2', children: [{ id: 5, label: '部门2-1' }] },
				{ id: 3, label: '部门3', children: [{ id: 6, label: '部门3-1' }] },
			],
			sortMethod: '',
			sortProp: '',
			tableData: [
				{
					id: 1,
					name: '张三',
					age: 24,
					address: '北京市朝阳区',
				},
				{
					id: 2,
					name: '李四',
					age: 28,
					address: '上海市浦东新区',
				},
				// ... 更多数据
			],
		};
	},
	computed: {
		filteredData() {
			let data = this.tableData;

			if (this.search) {
				data = data.filter((row) => row.name.includes(this.search));
			}

			if (this.sortMethod && this.sortProp) {
				data = data.sort((a, b) => {
					if (this.sortMethod === 'ascending') {
						return a[this.sortProp] > b[this.sortProp] ? 1 : -1;
					} else {
						return a[this.sortProp] < b[this.sortProp] ? 1 : -1;
					}
				});
			}

			// 添加根据 departmentId 过滤数据的逻辑
			if (this.selectedDepartmentId) {
				data = data.filter(
					(row) => row.departmentId === this.selectedDepartmentId
				);
			}


			return data;
		},
	},
	methods: {
		handleDepartmentChange(nodeData) {
			this.selectedDepartmentId = nodeData.id;
		},
		handleSearch() {
			// 当搜索框内容改变时触发
		},
		handleSortChange({ prop, order }) {
			this.sortMethod = order;
			this.sortProp = prop;
		},
		handleAdd() {
			// 添加新用户的逻辑
		},
		handleEdit(row) {
			// 编辑用户的逻辑
		},
		handleDelete(row) {
			// 删除用户的逻辑
		},
	},
};
</script>
  
<style scoped>
.main-box {
	width: 100%;
	padding: 24px;
	box-sizing: border-box;
}

.tree-filter {
	width: 240px;
	margin-right: 24px;
}

.table-box {
	flex: 1;
}

.table-header {
	display: flex;
	justify-content: space-between;
	margin-bottom: 12px;
}

.table-header input {
	width: 240px;
}
</style>