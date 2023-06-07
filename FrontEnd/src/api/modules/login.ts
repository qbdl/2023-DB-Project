import { Login, ResultData } from "@/api/interface/index";
import { PORT1,PORT3 } from "@/api/config/servicePort";
import DynamicRouter from "@/assets/json/dynamicRouter.json";
import AuthButtons from "@/assets/json/authButtons.json";
import qs from "qs";
import http from "@/api";
import { GlobalStore } from "@/stores";

/**
 * @name 登录模块
 */
// * 用户登录
export const my_loginApi=(username:any,password:any)=>{
	console.log("username:",username);
	console.log("password:",password);
	return http.post(PORT1 + `/login`,{"username":username,"password":password});
}



export const loginApi = (params: Login.ReqLoginForm) => {
	return http.post<Login.ResLogin>(PORT1 + `/login`, params, { headers: { noLoading: true } }); // 正常 post json 请求  ==>  application/json
	return http.post<Login.ResLogin>(PORT1 + `/login`, params, { headers: { noLoading: true } }); // 控制当前请求不显示 loading
	return http.post<Login.ResLogin>(PORT1 + `/login`, {}, { params }); // post 请求携带 query 参数  ==>  ?username=admin&password=123456
	return http.post<Login.ResLogin>(PORT1 + `/login`, qs.stringify(params)); // post 请求携带表单参数  ==>  application/x-www-form-urlencoded
	return http.get<Login.ResLogin>(PORT1 + `/login?${qs.stringify(params, { arrayFormat: "repeat" })}`); // 如果是 get 请求可以携带数组等复杂参数
};

// * 获取按钮权限
export const getAuthButtonListApi = () => {
	return http.get<Login.ResAuthButtons>(PORT1 + `/auth/buttons`, {}, { headers: { noLoading: true } });
	// 如果想让按钮权限变为本地数据，注释上一行代码，并引入本地 authButtons.json 数据

	return AuthButtons;
};

//判断权限
export const hasPermission = (route: any, roles: Array<string>) => {
	// if (route.children && route.children.length > 0) {
	// 	return true;
	// }
	if (route.meta && route.meta.roles) {
		return roles.some(role => route.meta.roles.includes(role));
	} else {
		return false;
	}
};

//根据权限筛选
export const filterAsyncRoutes = (routes: Array<any>, roles: Array<string>) => {
	console.log("routes = ", routes, "roles = ", roles);
	const res: Array<any> = [];
	routes.forEach(route => {
		const temp = { ...route };
		if (hasPermission(temp, roles)) {
			if (temp.children) {
				temp.children = filterAsyncRoutes(temp.children, roles);
			}
			res.push(temp);
		}
	});
	return res;
};

// * 获取菜单列表
export const getAuthMenuListApi = () => {
	// return http.get<Menu.MenuOptions[]>(PORT1 + `/menu/list`, {}, { headers: { noLoading: true } });
	// 如果想让菜单变为本地数据，注释上一行代码，并引入本地 dynamicRouter.json 数据
	// 动态过滤路由，根据meta项的roles属性过滤，roles项设置在最底层子路由上
	return new Promise<ResultData<Menu.MenuOptions[]>>(resolve => {
		const globalStore = GlobalStore();
		const accessRoutes = filterAsyncRoutes(DynamicRouter.data, globalStore.userInfo?.roles);
		console.log("userInfo = ", globalStore.userInfo);
		resolve({ code: "200", data: accessRoutes, msg: "success" });
		console.log({ accessRoutes });
	});
	return DynamicRouter;
};

// * 用户退出登录
export const logoutApi = () => {
	return http.post(PORT1 + `/logout`);
};
