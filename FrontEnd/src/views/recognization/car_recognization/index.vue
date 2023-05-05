<template>
    <div class="wrapper">
        <div class="main-container">
            <div class="header">
                <h1 class="text">车辆识别</h1>
            </div>
            <div class="out-div">
                <div class="image-container">
                    <img :src="selectedImage" alt="车辆图片" v-if="selectedImage" class="image-style" />
                    <span v-else>请上传车辆图片</span>
                </div>
                <div class="buttons">
                    <el-upload class="upload-demo" action="" :auto-upload="false" :on-change="handleImageChange">
                        <el-button size="mid" type="primary">选择图片</el-button>
                    </el-upload>
                    <el-button @click="recognizeVehicle">识别车辆</el-button>
                </div>
                <div class="result">
                    <p>识别结果：</p>
                    <textarea class="result-text" v-model="resultText" readonly></textarea>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import { ref } from "vue";

export default {
    setup() {
        const selectedImage = ref(null);
        const resultText = ref("");

        const handleImageChange = (file) => {
            const reader = new FileReader();
            reader.readAsDataURL(file.raw);
            reader.onload = (event) => {
                selectedImage.value = event.target.result;
            };
        };

        const recognizeVehicle = () => {
            // 在这里添加识别车辆的逻辑
            resultText.value = "未查到该车辆信息";
        };

        return {
            selectedImage,
            resultText,
            handleImageChange,
            recognizeVehicle,
        };
    },
};
</script>
  
<style scoped>
.wrapper {
    /* background-image: url("@/assets/images/background.png"); */
    width: 100%;
    height: 100%;
    z-index: -1;
}

.main-container {
    background-image: url("@/assets/images/background.png");
    /* background-image: url("@/assets/images/welcome_ori.png"); */
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f8f8f8;
    padding: 20px;
    border-radius: 15px;

    /* 新增属性 */
    background-size: cover;
    /* 缩放图片以完全覆盖容器，保持图片比例 */
    /* background-position: center; */
    /* 将图片居中显示 */
}

.header {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
}

.text {
    font-size: 35px;
    margin-bottom: 20px;
}

.out-div {
    display: flex;
    flex-direction: column;
    align-items: center;
    /* background-color: #ffffff; */
    background-color: rgba(255, 255, 255, 0.6);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.image-container {
    height: 400px;
    width: 500px;
    display: flex;
    justify-content: center;
    align-items: center;
    /* background-color: #f0f0f0; */
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 20px;
}

.image-style {
    max-height: 100%;
    max-width: 100%;
}

.buttons {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    width: 100%;
    margin: 20px 0;
}

.result {
    width: 100%;
}

.result-text {
    width: 100%;
    height: 100px;
    border-radius: 5px;
}
</style>  