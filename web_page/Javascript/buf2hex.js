const buf2hex = arrayBuffer => {
	return [...new Uint8Array(arrayBuffer)]
					.map(x => x.toString(16).padStart(2, '0')).join('');
}