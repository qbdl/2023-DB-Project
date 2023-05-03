<template>
	<div class="out-div">
		<p class="text">Lorem, ipsum dolor.</p>
		<video class="video-style" ref="videoElement"></video>
		<div class="buttons">
			<el-button @click="startVideo">开始视频</el-button>
			<el-button @click="detectFace">检测人脸</el-button>
			<el-button @click="recognizeFace">识别人脸</el-button>
		</div>
		<div class="result">
			<p>识别结果：</p>
			<textarea class="result-text" ref="resultText" readonly></textarea>
		</div>
	</div>
</template>
  
<script>
import { ref, onMounted } from "vue";
import * as faceapi from "face-api.js";

export default {
	setup() {
		const videoElement = ref(null);
		const resultText = ref(null);

		onMounted(async () => {
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

		let detectFace = async function () {
			const displaySize = { width: 1280, height: 720 };
			const detections = await faceapi
				.detectAllFaces(videoElement.value, new faceapi.TinyFaceDetectorOptions())
				.withFaceLandmarks()
				.withFaceDescriptors();

			const resizedDetections = faceapi.resizeResults(detections, displaySize);

			resultText.value = `检测到 ${resizedDetections.length} 张人脸。`;
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

			resultText.value = results.map(result => result.toString()).join('\n');
		};

		function loadLabeledImages() {
			// 在这里添加已标记的图像，如：{ name: "张三", imgSrc: "/labeled-images/zhangsan/1.jpg" }
			const labeledImages = [
				{
					name: "张三",
					imgSrc: "../../../labeled-images/zhangsan/userpic.jpg",
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
					descriptions.push(detections.descriptor);

					return new faceapi.LabeledFaceDescriptors(labeledImage.name, descriptions);
				})
			);
		}

		return {
			startVideo,
			detectFace,
			recognizeFace,
			videoElement,
			resultText,
		};
	},
};
</script>

<style scoped>
.out-div {
	display: flex;
	flex-direction: column;
	align-items: center;
}

.video-style {
	height: 500px;
	width: 500px;
}

.buttons {
	display: flex;
	justify-content: space-between;
	width: 100%;
	margin: 20px 0;
}

.result {
	width: 100%;
}

.result-text {
	width: 100%;
	height: 200px;
}
</style>

  