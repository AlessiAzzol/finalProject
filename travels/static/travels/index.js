document.addEventListener('DOMContentLoaded', function() {

	fetch("/homePage")
	.then(response => response.json())
	.then(info => {	
		for(i=0; i<info.links.length; i++){
			if( i!=0 && i % 3 == 0){
				const line = document.createElement('div') ;
				Object.assign(line, {
					className: "w-100"
				})	
				document.querySelector('#pictures').append(line);
			}
			const scene  = document.createElement('div') ;
			Object.assign(scene, {
				className: "scene col"
			})
			scene.innerHTML = `<div id="${info.info[i].name}" class="card" ><div id="front" class="front"><img src="${info.links[i].mobile}"></div><div class="back">${info.info[i].name}</div></div>`;
			document.querySelector('#pictures').append(scene);
		}
		
	});
});
