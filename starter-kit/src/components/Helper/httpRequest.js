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
	}
}

export default httpRequest;
