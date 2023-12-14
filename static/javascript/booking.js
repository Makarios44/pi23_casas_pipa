        var selectedRoom = document.getElementById("roomOptions");
		var booking = document.getElementById("booking");
		var roomDescription = document.getElementById("roomDescription");
		booking.style.backgroundImage = "url(images/customer-banner.jpg)";
		selectedRoom.onclick = function(){
			if (this.value == "deluxe"){
				booking.style.backgroundImage = "url(images/salasiba.jpg)";
				roomDescription.innerHTML = 'The room features a king size bed. Room also includes mini fridge, sofa, air conditioning, Wi-Fi, remote-controlled flat screen TV';

			}
			else if (this.value == "twin"){
				booking.style.backgroundImage = "url(images/IMG_3537.jpg)";
				roomDescription.innerHTML = 'The room features two separate standard  beds. Room also includes mini fridge, sofa air conditioning,  remote-controlled flat screen TV';
			}
			else if (this.value == "standard"){
				booking.style.backgroundImage = "url(images/sala.jpg)";
				roomDescription.innerHTML = 'The room features a bed (standard-size bed). Room also includes air conditioning, remote-controlled flat screen TV';
			}
			else {
				booking.style.backgroundImage = "url(images/hotelheaderscr.jpg)";
				roomDescription.innerHTML = '';
			}
		}