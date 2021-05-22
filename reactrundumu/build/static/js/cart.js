import React from 'react';


class Quantity extends React.Component {
    constructor() {
        super()
        this.addCookieItem = this.addCookieItem.bind(this)
        this.updateUserOrder = this.updateUserOrder.bind(this)
    }

    state = {
        quantity : 0
    }
    render() { 
        return (
            <>
                <span className="badge badge-secondary badge-sm m-2">{this.state.quantity}</span>
            </>
         );
    }
}
 
export default Quantity;


var updateBtns = document.getElementsByClassName('update-cart')


for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('USER: ', user)

        if(user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
} 

function addCookieItem(productId, action) {
    console.log('User is not authenticated')
    if (action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity' : 1}
            this.state.quantity = 1
        }else{
            cart[productId]['quantity'] += 1
            this.state.quantity += 1
        }
    }

    if (action == 'remove'){
        cart[productId]['quantity'] -= 1
        this.state.quantity -= 1

        if (cart[productId]['quantity'] <= 0){
            this.state.quantity = 0
            console.log('Item should be deleted.')
            delete cart[productId];
        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}
// passes cart data to the backend
function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
           console.log(response)
		   return response.json();
           
		})
		.then((data) => {
            console.log(data)
		    location.reload();
		})
        .catch(function(error) {
            console.error("Something");
            console.error(error);
        });
}