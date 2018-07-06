//npm install --save isomorphic-fetch es6-promise
import fetch from 'isomorphic-fetch';
const httpRequest = {
	post: (url, data) => {
		var result;
		result = fetch(url).then((Response) => Response.json()).then((findresponse) => {
                return findresponse;
            }
        );
		return result;
	},
	get: (url) => {
		var data;
		data = fetch(url).then((Response) => Response.json()).then((findresponse) => {
		
                return findresponse;
            }
        );
		return data;
	},
	getHtml:(url) =>{
	
		return fetch(url).then(function(res) {
			return res.text();
		}).then(function(html) {
			//console.log(`html = ${html}`);
			return html;
		});

	}
}

export default httpRequest;
