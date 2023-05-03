<template>
    <div class="main-container">
        <div class="left-panel">
            <el-select v-model="selectedOwner" placeholder="请选择业主特征信息" @change="handleOwnerChange">
                <el-option v-for="item in owners" :key="item.id" :label="item.name" :value="item"></el-option>
            </el-select>
        </div>
        <div class="right-panel">
            <div class="owner-card" v-if="selectedOwner">
                <div class="header">
                    <h2>{{ selectedOwner.name }}</h2>
                </div>
                <!-- Add avatar container and input for uploading image -->
                <div class="avatar-container">
                    <img :src="selectedOwner.avatar || defaultAvatar" class="avatar">
                    <input v-if="editing" type="file" @change="uploadImage" ref="fileInput">
                </div>
                <el-descriptions class="table_user" title="个人信息" direction="vertical" :column="2" :size="'large'" border>
                    <el-descriptions-item label="用户名">
                        <el-input v-model="selectedOwner.username" :disabled="!editing"></el-input>
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
import { ref } from "vue";

export default {
    name: "ownerInfo",
    setup() {
        let editing = ref(false);
        let fileInput = ref(null);
        let defaultAvatar = "../../assets/images/userpic.jpg"; // Set the URL of the default avatar image

        const owners = [
            {
                id: 1,
                name: "张三",
                username: "zhangsan",
                phone: "13912345678",
                address: "上海市浦东新区",
                email: "zhangsan@example.com",
                communityName: "阳光花园",
                buildingNumber: "5栋",
                unitNumber: "2单元",
                doorNumber: "502室",
                parkingNumber: "B-102",
                securityCardNumber: "AF-123456",
                emergencyContact: "李四",
                emergencyContactPhone: "18212345678",
            },
            {
                id: 2,
                name: "李四",
                username: "lisi",
                phone: "13923456789",
                address: "上海市浦东新区",
                email: "lisi@example.com",
                communityName: "阳光花园",
                buildingNumber: "3栋",
                unitNumber: "1单元",
                doorNumber: "301室",
                parkingNumber: "B-103",
                securityCardNumber: "AF-123457",
                emergencyContact: "王五",
                emergencyContactPhone: "13934567890",
            },
            // 更多业主信息
        ];


        let selectedOwner = ref(null);

        let handleOwnerChange = function (selected) {
            selectedOwner.value = selected;
        };

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
                    selectedOwner.value.avatar = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        };

        return {
            owners,
            selectedOwner,
            handleOwnerChange,
            editProfile,
            editing,
            fileInput,
            uploadImage,
            defaultAvatar,
        };
    },
};
</script>
  
<style scoped lang="scss">
.main-container {
    display: flex;
    flex-direction: row;
}

.left-panel {
    width: 20%;
    padding: 20px;
}

.right-panel {
    width: 80%;
    padding: 20px;
}

.avatar-container {
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
}

.avatar {
    width: 100px;
    height: 100px;
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
    margin-bottom: 20px;
}

.avatar-container {
    margin-bottom: 20px;
}

.table_user {
    width: 85%;
    margin-bottom: 20px;
}
</style>
  