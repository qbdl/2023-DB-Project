<template>
    <div class="main-container">
        <div class="card">
            <div class="header">
                <h2>个人信息管理</h2>
            </div>
            <!-- Add avatar container and input for uploading image -->
            <div class="avatar-container">
                <img :src="defaultAvatar || avatar_path" class="avatar">
                <input v-if="editing" type="file" @change="uploadImage" ref="fileInput">
            </div>

            <!-- 描述性列表 -->
            <el-descriptions class="table_user" title="个人信息" direction="vertical" :column="2" size="large" border>
                <el-descriptions-item label="用户名">
                    <el-input v-model="username" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="性别">
                    <el-input v-model="gender" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="身份证号">
                    <el-input v-model="idCard" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="电话">
                    <el-input v-model="phone" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="地址" :span="2">
                    <el-input v-model="address" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="邮箱">
                    <el-input v-model="email" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="小区名称">
                    <el-input v-model="communityName" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="楼栋号">
                    <el-input v-model="buildingNumber" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="单元号">
                    <el-input v-model="unitNumber" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="门牌号">
                    <el-input v-model="doorNumber" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="车位号">
                    <el-input v-model="parkingNumber" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="安防卡号">
                    <el-input v-model="securityCardNumber" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="紧急联系人">
                    <el-input v-model="emergencyContact" :disabled="!editing"></el-input>
                </el-descriptions-item>
                <el-descriptions-item label="紧急联系电话">
                    <el-input v-model="emergencyContactPhone" :disabled="!editing"></el-input>
                </el-descriptions-item>
            </el-descriptions>

            <el-button @click="editProfile" class="action-btn">{{ editing ? '保存' : '编辑个人信息' }}</el-button>
        </div>
    </div>
</template>

<script lang="js">
import { ref, onMounted } from "vue";
import axios from "axios"; // 导入 axios 库——用于向后端发出 HTTP 请求，以获取和发送数据
import { ElMessage } from "element-plus";

export default {
    name: "personalInfo",
    setup() {
        let size = ref("small");
        let fileInput = ref(null);
        let editing = ref(false);

        let defaultAvatar = "../../assets/images/userpic.jpg";
        let owner_id = ref(null);
        let username = ref(null); // 初始化为 null
        let phone = ref(null); // 初始化为 null
        let address = ref(null); // 初始化为 null
        let email = ref(null); // 初始化为 null
        let communityName = ref(null); // 初始化为 null
        let buildingNumber = ref(null); // 初始化为 null
        let unitNumber = ref(null); // 初始化为 null
        let doorNumber = ref(null); // 初始化为 null
        let parkingNumber = ref(null); // 初始化为 null
        let securityCardNumber = ref(null); // 初始化为 null
        let emergencyContact = ref(null); // 初始化为 null
        let emergencyContactPhone = ref(null); // 初始化为 null
        let avatar_path = ref("../../assets/images/userpic.jpg")//初始化为../../assets/images/userpic.jpg
        let faceInfo_path = ref("../../assets/images/userpic.jpg")//初始化为../../assets/images/userpic.jpg
        let gender = ref(null);
        let idCard = ref(null);
        let createTime = ref(null);
        let status = ref(null);

        let editProfile = async function () {
            editing.value = !editing.value;
            if (!editing.value) {
                // Save the updated profile here
                const data = {
                    owner_id: owner_id.value,
                    username: username.value,
                    phone: phone.value,
                    address: address.value,
                    email: email.value,
                    communityName: communityName.value,
                    buildingNumber: buildingNumber.value,
                    unitNumber: unitNumber.value,
                    doorNumber: doorNumber.value,
                    parkingNumber: parkingNumber.value,
                    securityCardNumber: securityCardNumber.value,
                    emergencyContact: emergencyContact.value,
                    emergencyContactPhone: emergencyContactPhone.value,
                    avatar_path: avatar_path.value,
                    gender: gender.value,
                    idCard: idCard.value,
                    createTime: createTime.value,
                    status: status.value,
                    faceInfo_path:faceInfo_path.value,
                };
                //传回给后端数据库
                try {
                    await axios.put("http://localhost:5000/user/info_update", data);
                    ElMessage({ message: "个人信息更新成功", type: "success" });
                } catch (error) {
                    console.error(error);
                    ElMessage({ message: "个人信息更新失败，请重试", type: "error" });
                }
            }
        };

        //上传头像
        const uploadImage = async (event) => {
            const file = event.target.files[0];
            if (file) {
                const formData = new FormData();
                formData.append("file", file);
                try {
                    await axios.post("http://localhost:5000/upload/upload_avatar", formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        },
                        params:
                            { owner_id: 1 } // TODO:修改为个人信息ID
                    });
                    avatar_path.value = URL.createObjectURL(file);
                    // avatar_path.value = response.data.avatar_path;
                    ElMessage({ message: "头像上传成功", type: "success" });
                } catch (error) {
                    console.error(error);
                    ElMessage({ message: "头像上传失败，请重试", type: "error" });
                }
            }
        };


        // 从后端获取初始数据
        const fetchData = async () => {
            try {
                const response = await axios.get("http://localhost:5000/user/info",
                    {
                        params:
                            { is_owner: 0 } //用户个人信息
                    });
                const data = response.data;
                owner_id.value = data.owner_id;
                username.value = data.username;
                phone.value = data.phone;
                address.value = data.address;
                email.value = data.email;
                communityName.value = data.communityName;
                buildingNumber.value = data.buildingNumber;
                unitNumber.value = data.unitNumber;
                doorNumber.value = data.doorNumber;
                parkingNumber.value = data.parkingNumber;
                securityCardNumber.value = data.securityCardNumber;
                emergencyContact.value = data.emergencyContact;
                emergencyContactPhone.value = data.emergencyContactPhone;
                avatar_path.value = data.avatar_path;
                gender.value = data.gender;
                idCard.value = data.idCard;
                createTime.value = data.createTime;
                status.value = data.status;
                faceInfo_path.value=data.faceInfo_path;
            } catch (error) {
                console.error(error);
            }
        };
        // 在组件挂载时从后端获取数据
        onMounted(fetchData);//生命周期钩子，在组件挂载时调用 fetchData 函数，以便在页面加载时自动获取数据。

        return {
            size,
            fileInput,
            editing,
            defaultAvatar,
            owner_id,
            username,
            phone,
            address,
            email,
            communityName,
            buildingNumber,
            unitNumber,
            doorNumber,
            parkingNumber,
            securityCardNumber,
            emergencyContact,
            emergencyContactPhone,
            editProfile,
            uploadImage,
            avatar_path, 
            gender,
            idCard,
            createTime,
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
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f8f8f8;
    padding: 20px;
    border-radius: 15px;

    background-size: cover;

}

.card {
    background-color: rgba(255, 255, 255, 0.8);
    width: 80%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    font-size: 1.4em;
}

.header {
    width: 100%;
    text-align: center;
    margin-bottom: 20px;
}

.avatar {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 10px;
}

.table_user {
    width: 85%;
    margin-bottom: 20px;
}


.action-btn {
    margin-bottom: 10px;
}
</style>