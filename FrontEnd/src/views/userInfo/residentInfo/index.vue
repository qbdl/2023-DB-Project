<template>
    <div class="card">
        <div class="header">
            <h2>个人信息管理</h2>
        </div>
        <!-- Add avatar container and input for uploading image -->
        <div class="avatar-container">
            <img :src="avatar || defaultAvatar" class="avatar">
            <input v-if="editing" type="file" @change="uploadImage" ref="fileInput">
        </div>

        <!-- 描述性列表 -->
        <el-descriptions class="table_user" title="个人信息" direction="vertical" :column="2" :size="Large" border>
            <el-descriptions-item label="用户名">
                <el-input v-model="username" :disabled="!editing"></el-input>
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
</template>

<script lang="js">
import { ref } from "vue";

export default {
    name: "personalInfo",
    setup() {
        let size = ref("small");
        let fileInput = ref(null);
        let editing = ref(false);

        let avatar = ref("../../assets/images/userpic.jpg")
        let defaultAvatar = "../../assets/images/userpic.jpg"; // Set the URL of the default avatar image
        let username = ref("qbdl");
        let phone = ref("18105022730");
        let address = ref("苏州市吴中区吴中大道1188号");
        let email = ref("likejie@tongji.edu.cn");
        let communityName = ref("阳光花园");
        let buildingNumber = ref("5栋");
        let unitNumber = ref("2单元");
        let doorNumber = ref("502室");
        let parkingNumber = ref("B-102");
        let securityCardNumber = ref("AF-123456");
        let emergencyContact = ref("张三");
        let emergencyContactPhone = ref("18212345678");

        let editProfile = function () {
            editing.value = !editing.value;
            if (!editing.value) {
                // Save the updated profile here
                // e.g. send the updated data to the server via API call
            }
        };

        let uploadImage = function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    avatar.value = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        };

        return {
            size,
            fileInput,
            editing,
            avatar,
            defaultAvatar,
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
        };

    },
};
</script>

<style scoped lang="scss">
.card {
    width: 100%;
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
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 20px;
}

.table_user {
    width: 75%; //100%
    margin-bottom: 20px;
    margin-left: 200px;
    margin-right: 200px;
    font-size: 2.0em;
}


.action-btn {
    margin-bottom: 10px;
}
</style>