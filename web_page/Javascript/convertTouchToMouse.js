"use strict";

/**
	* このプログラムは、touchのイベントが発火した際に、対応するmouseイベントを発火するプログラムです。
	* pygameをトランスコンパイルして実行した際、touchイベントへの対応がなかったため、このファイルを使用してタッチ動作を実現します。
	*/

const LEFT_MOUSE_BUTTON = 0
const RIGHT_MOUSE_BUTTON = 2
const TOUCH_POS_INDEX = 0

let touchTimeStamp = 0

const intervalId = setInterval(() => {
	const canvas = document.getElementsByTagName("canvas")[0]
	if (canvas) {
		canvas.addEventListener("touchmove", (event) => {
			const mouseMoveEvent = new MouseEvent('mousemove', {
				bubbles: true,
				cancelable: true,
				button: LEFT_MOUSE_BUTTON,
				clientX: event.changedTouches[TOUCH_POS_INDEX].pageX,
				clientY: event.changedTouches[TOUCH_POS_INDEX].pageY
			});
			canvas.dispatchEvent(mouseMoveEvent);
		})

		canvas.addEventListener("touchend", (event) => {
			if (event.timeStamp - touchTimeStamp > 500) {
				const mouseUpEvent = new MouseEvent('mouseup', {
					bubbles: true,
					cancelable: true,
					button: LEFT_MOUSE_BUTTON,
					clientX: event.changedTouches[TOUCH_POS_INDEX].pageX,
					clientY: event.changedTouches[TOUCH_POS_INDEX].pageY
				});
				canvas.dispatchEvent(mouseUpEvent);
			}
		})

		canvas.addEventListener("touchstart", (event) => {
			//	前回のtouchstartから250ms以内にtouchstartが発火した場合、右クリックとして扱う
			if (event.timeStamp - touchTimeStamp < 250) {
				const rightMouseDownEvent = new MouseEvent('mousedown', {
					bubbles: true,
					cancelable: true,
					button: RIGHT_MOUSE_BUTTON,
					clientX: event.touches[TOUCH_POS_INDEX].pageX,
					clientY: event.touches[TOUCH_POS_INDEX].pageY
				});
				event.preventDefault()
				canvas.dispatchEvent(rightMouseDownEvent);
			} else {
				const mouseDownEvent = new MouseEvent('mousedown', {
					bubbles: true,
					cancelable: true,
					button: LEFT_MOUSE_BUTTON,
					clientX: event.touches[TOUCH_POS_INDEX].pageX,
					clientY: event.touches[TOUCH_POS_INDEX].pageY
				});
				canvas.dispatchEvent(mouseDownEvent);
				touchTimeStamp = event.timeStamp
			}
		})

		clearInterval(intervalId)
	}
}, 100)