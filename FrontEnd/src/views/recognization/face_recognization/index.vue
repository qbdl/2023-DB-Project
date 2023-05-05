<template>
    <div class="wrapper">
        <div class="main-container">
            <div class="header">
                <h1 class="text">人脸检测与识别</h1>
            </div>
            <div class="out-div">
                <video class="video-style" ref="videoElement"></video>
                <div class="buttons">
                    <el-button @click="startVideo">开始视频</el-button>
                    <el-button @click="stopVideo">结束视频</el-button>
                    <el-button @click="detectFace">检测人脸</el-button>
                    <el-button @click="recognizeFace">识别人脸</el-button>
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
import { ref, onMounted } from "vue";
import * as faceapi from "face-api.js";
// import { require } from "module";
// import { text } from 'stream/consumers';

export default {
    setup() {
        const videoElement = ref(null);
        // const resultText = ref(null);
        const resultText = ref('');


        onMounted(async () => {
            await faceapi.nets.ssdMobilenetv1.load('/models');
            await faceapi.nets.tinyFaceDetector.load("/models");
            await faceapi.nets.faceRecognitionNet.load("/models");
            await faceapi.nets.faceLandmark68Net.load("/models");
        });

        // 开始视频，调用摄像头
        let startVideo = function () {
            var constraints = { audio: true, video: { width: 1280, height: 720 } };
            navigator.mediaDevices
                .getUserMedia(constraints)
                .then(function (mediaStream) {
                    videoElement.value.srcObject = mediaStream;
                    videoElement.value.onloadedmetadata = function (e) {
                        videoElement.value.play();
                    };
                })
                .catch(function (err) {
                    console.log(err.name + ": " + err.message);
                }); // 总是在最后
        };

        // 结束视频
        let stopVideo = function () {
            if (videoElement.value.srcObject) {
                const tracks = videoElement.value.srcObject.getTracks();
                tracks.forEach((track) => {
                    track.stop();
                });
                videoElement.value.srcObject = null;
            }
        };

        let detectFace = async function () {
            const displaySize = { width: 1280, height: 720 };
            const detections = await faceapi
                .detectAllFaces(videoElement.value, new faceapi.TinyFaceDetectorOptions())
                .withFaceLandmarks()
                .withFaceDescriptors();

            console.log('Detections:', detections);

            const resizedDetections = faceapi.resizeResults(detections, displaySize);
            resultText.value = `检测到 ${resizedDetections.length} 张人脸。`;

            // // Draw face bounding boxes
            // const canvas = document.createElement('canvas');
            // canvas.width = videoElement.value.width;
            // canvas.height = videoElement.value.height;
            // const context = canvas.getContext('2d');
            // context.clearRect(0, 0, canvas.width, canvas.height);
            // faceapi.draw.drawDetections(canvas, resizedDetections);
            // videoElement.value.parentNode.insertBefore(canvas, videoElement.value.nextSibling);
        };


        let recognizeFace = async function () {
            const labeledFaceDescriptors = await loadLabeledImages();
            const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6);

            const displaySize = { width: 1280, height: 720 };
            const detections = await faceapi
                .detectAllFaces(videoElement.value, new faceapi.TinyFaceDetectorOptions())
                .withFaceLandmarks()
                .withFaceDescriptors();

            const resizedDetections = faceapi.resizeResults(detections, displaySize);

            const results = resizedDetections.map(d => faceMatcher.findBestMatch(d.descriptor));

            console.log("Results:", results);
            resultText.value = results.map(result => `${result.label} (${(1 - result.distance).toFixed(2)})`).join('\n');

            console.log("value:", resultText.value);
            // resultText.value = results.map(result => result.toString()).join('\n');

        };

        function loadLabeledImages() {
            // 在这里添加已标记的图像，如：{ name: "张三", imgSrc: "/labeled-images/zhangsan/1.jpg" }
            const labeledImages = [
                // {
                //     name: "张三",
                //     imgSrc: "/assets/labeled-images/zhangsan/userpic.jpg",
                // },
                {
                    name: "Jack",
                    imgSrc: "/assets/labeled-images/Jack/Me1.jpg",
                },
                {
                    name: "Jack",
                    imgSrc: "/assets/labeled-images/Jack/Me2.jpg",
                },
                {
                    name: "Jack",
                    imgSrc: "/assets/labeled-images/Jack/Me3.jpg",
                },

                // ...
            ];

            return Promise.all(
                labeledImages.map(async (labeledImage) => {
                    const descriptions = [];
                    const img = await faceapi.fetchImage(labeledImage.imgSrc);
                    const detections = await faceapi
                        .detectSingleFace(img)
                        .withFaceLandmarks()
                        .withFaceDescriptor();

                    if (detections) { // 检查detections是否存在
                        descriptions.push(detections.descriptor);
                    } else {
                        console.warn(`无法检测到人脸: ${labeledImage.name}`);
                    }

                    return new faceapi.LabeledFaceDescriptors(labeledImage.name, descriptions);
                })
            );
        }

        return {
            startVideo,
            stopVideo,
            detectFace,
            recognizeFace,
            videoElement,
            resultText,
            // imgSrc: require('../../assets/images/userpic.jpg'),
        };
    },
};
</script>


<style scoped>
.wrapper {
    background-size: 100% 100%;
    width: 100%;
    height: 100%;
    /**宽高100%是为了图片铺满屏幕 */
    z-index: -1;
}

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
    background-color: rgba(255, 255, 255, 0.8);
    /* 修改背景颜色，添加透明度 */
    /* background-color: #ffffff; */
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.video-style {
    height: 400px;
    width: 500px;
    border-radius: 10px;
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