// import React, { useState } from 'react';
// import './Camera.css';

// function Camera() {
// 	const [playing, setPlaying] = useState(false);
// 	localStorage.setItem("startCamera", true);
// 	const HEIGHT = 500;
// 	const WIDTH = 500;

// 	const startVideo = () => {
// 		localStorage.setItem("startCamera",true);
// 		let currentStatus = localStorage.getItem("startCamera")
// 		setPlaying(currentStatus);
// 		navigator.getUserMedia(
// 			{
// 				video: true,
// 			},
// 			(stream) => {
// 				let video = document.getElementsByClassName('app__videoFeed')[0];
// 				if (video) {
// 					video.srcObject = stream;
// 				}
// 			},
// 			(err) => console.error(err)
// 		);
// 	};

// 	const stopVideo = () => {
// 		let currentStatus = localStorage.setItem("startCamera", false);
// 		setPlaying(currentStatus);
// 		let video = document.getElementsByClassName('app__videoFeed')[0];
// 		video.srcObject.getTracks()[0].stop();
// 	};
// 	console.log("trang thai cam " , localStorage.getItem("startCamera"));
// 	return (
// 		<div className="app"
// 			 >
// 			<div className="app__container">
// 				<video
// 					height={HEIGHT}
// 					width={WIDTH}
// 					muted
// 					autoPlay
// 					className="app__videoFeed"
// 				></video>
// 			</div>
// 			<div className="app__input">
// 				{ playing ? (
// 					<button onClick={stopVideo}>Stop</button>
// 				) : (
// 					<button onClick={startVideo}>Start</button>
// 				)}
// 			</div>
// 		</div>
// 	);
// }

// export default Camera;
