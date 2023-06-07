<template>
    <div class="main-container">
        <div class="left-panel">
            <el-select v-model="selectedOwner" placeholder="请选择业主特征信息" @change="handleOwnerChange">
                <el-option v-for=" item in owners" :key="item.id" :label="item.username" :value="item"></el-option>
            </el-select>
        </div>
        <div class="right-panel">
            <div class="owner-card" v-if="selectedOwner">
                <div class="header">
                    <h2>{{ selectedOwner.username }}</h2>
                </div>
                <!-- Add avatar container and input for uploading image -->
                <div class="avatar-container">
                    <img :src="defaultAvatar || selectedOwner.avatar_path" class="avatar">
                    <input v-if="editing" type="file" @change="uploadImage" ref="fileInput">
                </div>
                <el-descriptions class="table_user" title="业主具体信息" direction="vertical" :column="2" size="large" border>
                    <el-descriptions-item label="用户名">
                        <el-input v-model="selectedOwner.username" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="性别">
                        <el-input v-model="selectedOwner.gender" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="身份证号">
                        <el-input v-model="selectedOwner.idCard" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="电话">
                        <el-input v-model="selectedOwner.phone" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="地址" :span="2">
                        <el-input v-model="selectedOwner.address" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="邮箱">
                        <el-input v-model="selectedOwner.email" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="小区名称">
                        <el-input v-model="selectedOwner.communityName" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="楼栋号">
                        <el-input v-model="selectedOwner.buildingNumber" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="单元号">
                        <el-input v-model="selectedOwner.unitNumber" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="门牌号">
                        <el-input v-model="selectedOwner.doorNumber" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="车位号">
                        <el-input v-model="selectedOwner.parkingNumber" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="安防卡号">
                        <el-input v-model="selectedOwner.securityCardNumber" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="紧急联系人">
                        <el-input v-model="selectedOwner.emergencyContact" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                    <el-descriptions-item label="紧急联系电话">
                        <el-input v-model="selectedOwner.emergencyContactPhone" :disabled="!editing"></el-input>
                    </el-descriptions-item>
                </el-descriptions>
                <el-button @click="editProfile" class="action-btn">{{ editing ? '保存' : '编辑业主信息' }}</el-button>
            </div>
        </div>
    </div>
</template>
  
<script lang="js">
import { ref, onMounted } from "vue";
import axios from "axios"; // 导入 axios 库——用于向后端发出 HTTP 请求，以获取和发送数据
import { ElMessage } from "element-plus";

export default {
    name: "ownerInfo",
    setup() {
        let editing = ref(false);
        let fileInput = ref(null);
        let owners = ref(null);
        let defaultAvatar = "../../assets/images/userpic.jpg"; // Set the URL of the default avatar image
        let avatar_path = ref("../../assets/images/userpic.jpg");//初始化为../../assets/images/userpic.jpg
        let gender = ref(null);
        let idCard = ref(null);
        // let createTime = ref(null);
        let status = ref(null);
        let selectedOwner = ref(null);
        let faceInfo_path=ref("../../assets/images/userpic.jpg");

        //从后端获取 选择的业主信息
        let handleOwnerChange = async function () {
            try {
                const selectedId = selectedOwner.value.id; // 从当前选中的业主获取ID
                const response = await axios.get("http://localhost:5000/user/info",
                    {
                        params:
                            { is_owner: 1, owner_id: selectedId } // 业主信息
                    });
                selectedOwner.value = response.data;
                // console.log("getOwners data:", response.data);
                console.log("getOwners data:", selectedOwner.value);
            } catch (error) {
                console.error(error);
                ElMessage({ message: "无法获取业主信息，请重试", type: "error" });
            }
        };


        //按钮触发事件
        let editProfile = async function () {
            editing.value = !editing.value;
            if (!editing.value) {
                // Save the updated profile here
                // console.log("editProfile:", selectedOwner.value);
                // console.log(selectedOwner.value.id);
                const data = {
                    // owner_id: selectedOwner.value.owner_id,
                    idCard: selectedOwner.value.idCard,
                    username: selectedOwner.value.username,
                    phone: selectedOwner.value.phone,
                    address: selectedOwner.value.address,
                    email: selectedOwner.value.email,
                    communityName: selectedOwner.value.communityName,
                    buildingNumber: selectedOwner.value.buildingNumber,
                    unitNumber: selectedOwner.value.unitNumber,
                    doorNumber: selectedOwner.value.doorNumber,
                    parkingNumber: selectedOwner.value.parkingNumber,
                    securityCardNumber: selectedOwner.value.securityCardNumber,
                    emergencyContact: selectedOwner.value.emergencyContact,
                    emergencyContactPhone: selectedOwner.value.emergencyContactPhone,
                    avatar_path: selectedOwner.value.avatar_path,
                    gender: selectedOwner.value.gender,
                    // createTime: selectedOwner.value.createTime,
                    status: selectedOwner.value.status,
                    faceInfo_path: selectedOwner.value.faceInfo_path,
                };
                console.log("transfer to BackEnd data:",data);
                //传回给后端数据库
                try {
                    await axios.put("http://localhost:5000/user/info_update", data, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    ElMessage({ message: "业主信息更新成功", type: "success" });
                } catch (error) {
                    console.error(error);
                    ElMessage({ message: "业主信息更新失败，请重试", type: "error" });
                }
            }
        };


        let uploadImage = function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    selectedOwner.value.avatar_path = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        };


        // 从后端获取初始业主列表
        const fetchOwners = async () => {
            try {
                const response = await axios.get("http://localhost:5000/user/owners");
                // console.log('API response:', response.data); // 添加这一行
                owners.value = response.data;
                console.log("handleOwnerChange data:", response.data); // 添加此行
            } catch (error) {
                console.error(error);
            }
        };
        // 在组件挂载时从后端获取数据
        onMounted(fetchOwners);


        return {
            fileInput,
            defaultAvatar,
            editing,

            avatar_path,
            owners,
            selectedOwner,
            handleOwnerChange,
            editProfile,
            uploadImage,
            gender,
            idCard,
            // createTime,
            status,
            faceInfo_path,
        };
    },
};
</script>
  
<style scoped lang="scss">
.main-container {
    background-image: url("@/assets/images/background.png");
    z-index: 1;
    // align-items: center;
    background-color: #f8f8f8;
    padding: 20px;
    border-radius: 15px;

    background-size: cover;

    display: flex;
    flex-direction: row;
}

.left-panel {
    width: 20%;
    padding: 20px;
}

.right-panel {
    background-color: rgba(255, 255, 255, 0.8);
    ;
    width: 80%;
    padding: 20px;
}

.avatar-container {
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
}

.avatar {
    width: 130px;
    height: 130px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 10px;
}

.owner-card {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    font-size: 1.2em;
}

.header {
    width: 100%;
    text-align: center;
    margin-bottom: 10px;
}

.avatar-container {
    margin-bottom: 10px;
}

.table_user {
    width: 85%;
    margin-bottom: 20px;
}
</style>
  