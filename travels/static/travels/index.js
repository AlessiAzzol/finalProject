document.addEventListener('DOMContentLoaded', function() {

	fetch("/homePage")
	.then(response => response.json())
	.then(info => {	
		for(i=0; i<info.links.length; i++){
			const cards  = document.createElement('div') ;
			Object.assign(cards, {
				className: "cards col-lg-4",
				id: `${info.info[i].name}`
			})
			cards.innerHTML = `<div class="card-front"></div><div class="card-back"><h2>${info.info[i].name}</h2></div></div>`;
			document.querySelector('#pictures').append(cards);
			cards.querySelector(".card-front").style.backgroundImage = `url(${info.links[i].mobile})`;
		}
		
	});
});
