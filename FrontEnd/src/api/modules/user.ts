import { ResPage, User } from "@/api/interface/index";
import http from "@/api";
// import axios from "axios";

// const PORT1 = "/geeker";
const PORT1 = "";

// const interface ResUserList {
// 	id: string;
// 	username: string;
// 	gender: number;
// 	user: {
// 		detail: {
// 			age: number;
// 		};
// 	};
// 	idCard: string;
// 	email: string;
// 	address: string;
// 	createTime: string;
// 	status: number;
// 	avatar: string;
// 	children?: ResUserList[];
// }
/**
 * @name 用户管理模块
 */
// * 获取用户列表
export const getUserList = (params: User.ReqUserParams) => {
	// let temp = http.post<ResPage<User.ResUserList>>(PORT1 + `/user/list`, params);
	// console.log(temp);
	return http.post<ResPage<User.ResUserList>>(PORT1 + `/user/list`, params);
	// let T=ResPage<User.ResUserList>
	// return post<T>(url: string, params?: object, _object = {}): Promise<ResultData<T>> {
	// 	return this.service.post(url, params, _object);
	// }
	// return http.post<>(`/list`, params);
	// const url = "test";
	// const config = {
	// 	// 默认地址请求地址，可在 .env.*** 文件中修改
	// 	baseURL: import.meta.env.VITE_API_URL as string,
	// 	// 跨域时候允许携带凭证
	// 	withCredentials: true
	// };
	// let service = axios.create(config);
	// let data = service.post(url, params);
	// return data;

	// return axios.post(PORT1 + `/list`, params);
};

// * 获取树形用户列表
export const getUserTreeList = (params: User.ReqUserParams) => {
	return http.post<ResPage<User.ResUserList>>(PORT1 + `/user/tree/list`, params);
};

// * 新增用户
export const addUser = (params: { id: string }) => {
	return http.post(PORT1 + `/user/add`, params);
};

// * 批量添加用户
export const BatchAddUser = (params: FormData) => {
	return http.post(PORT1 + `/user/import`, params);
};

// * 编辑用户
export const editUser = (params: { id: string }) => {
	return http.post(PORT1 + `/user/edit`, params);
};

// * 删除用户
export const deleteUser = (params: { id: string[] }) => {
	return http.post(PORT1 + `/user/delete`, params);
};

// * 切换用户状态
export const changeUserStatus = (params: { id: string; status: number }) => {
	return http.post(PORT1 + `/user/change`, params);
};

// * 重置用户密码
export const resetUserPassWord = (params: { id: string }) => {
	return http.post(PORT1 + `/user/rest_password`, params);
};

// * 导出用户数据
export const exportUserInfo = (params: User.ReqUserParams) => {
	return http.download(PORT1 + `/user/export`, params);
};

// * 获取用户状态
export const getUserStatus = () => {
	return http.get<User.ResStatus>(PORT1 + `/user/status`);
};

// * 获取用户性别字典
export const getUserGender = () => {
	return http.get<User.ResGender>(PORT1 + `/user/gender`);
};

// * 获取用户部门列表
export const getUserDepartment = () => {
	return http.get<User.ResDepartment>(PORT1 + `/user/department`);
};

// * 获取用户角色字典
export const getUserRole = () => {
	return http.get<User.ResRole>(PORT1 + `/user/role`);
};
