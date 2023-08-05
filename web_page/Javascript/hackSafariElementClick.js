"use strict";
// ブラウザがSafariであるかどうか判定する
const isSafari = () => {
	const userAgent = window.navigator.userAgent.toLowerCase();
	return userAgent.indexOf('safari') !== -1 && userAgent.indexOf('chrome') === -1 && userAgent.indexOf('edge') === -1
}

// Safariのセキュリティポリシーにより、動的にピッカーを表示できないため、ダイアログを表示しユーザーに選択させる
// 選択させた内容は、メインプログラムの監視対象の要素に反映させ、チェンジイベントを発火させる。
// 監視対象の要素は、chromeなどで画面上に適切にピッカーを表示させるために、ダイアログとは違う場所に配置されている
const color_selector_hack = () => {
	const color_selector = document.getElementById("color_selector")

	const safari_color_picker_dialog = document.getElementById("safari_color_picker_dialog")
	const safari_color_picker = document.getElementById("safari_color_picker")
	const color_decide_button = document.getElementById("safari_color_picker_decide_button")

	color_selector.click = () => safari_color_picker_dialog.showModal()

	const color_select_caller = () => {
		const color = safari_color_picker.value
		color_selector.value = color
		const color_change_event = new Event("change", { bubbles: true })
		color_selector.dispatchEvent(color_change_event)
		safari_color_picker_dialog.close()
	}
	color_decide_button.addEventListener("click", color_select_caller)
	safari_color_picker_dialog.addEventListener("close", color_select_caller)
}

// Safariのセキュリティポリシーにより、動的にファイル選択画面を表示させることができないため、ダイアログを表示しユーザーに選択させる
// Safari以外は、dialogの中にあるfile selectorに向かってclickメッセージを送ることで、ファイル選択画面を表示させることができる。
// そのため、色選択の時と違い、監視対象の要素そのものをダイアログに入れている。
const file_selector_hack = () => {
	const file_selector = document.getElementById("file_selector")

	const safari_file_selector_dialog = document.getElementById("safari_file_selector_dialog")

	file_selector.click = () => safari_file_selector_dialog.showModal()

	file_selector.addEventListener("change", (e) => {
		safari_file_selector_dialog.close()
	})
}

if (isSafari()) {
	color_selector_hack()
	file_selector_hack()
}