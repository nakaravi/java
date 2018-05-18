import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import {getData} from '../reducers/services';


/*  const personLoc = Object.keys(this.state.json).map((content, idx) => {
		const items = this.state.json[content].map((item, i) => (
			<p key={i}>{item.title}</p>
		))

		return <div key={idx}>{items}</div>
	});
	*/
	function Listitem(data){
		
		return '<div>List Item displays here</div>';
	}
export default class PlacePage extends React.Component{

	
	constructor(props){
		super(props);
		this.state = {json:[], paging:[]};
	}
	
	getInitialState() {
		return {
		  json: Map({ title: 0 }),
		  paging:Map({ page: 1 }),
		}
	  }

	componentDidMount() {
		let that = this;
		let url = "http://localhost/api/product/read_paging.php";//"http://www.androidbegin.com/tutorial/jsonparsetutorial.txt";//
		
		
		
		fetch(url)
		.then(response => response.json())
		.then(responseJson => {
			console.log(responseJson.paging.pages);
			that.setState({json : responseJson.records,paging:responseJson.paging.pages});
			//that.json = responseJson.records;
			//console.log(that.json);
			//return responseJson.movies;
			/* Object.keys(paging).map((content, idx) => {
				return <span className="page">{idx+1}</span>
			})  */
		})
		.catch(error => {
			console.error(error);
		});
	}
	
	onClickDetail(idx) {
		this.props.history.push('/detail/' + idx);
	}
	
	pagination(idx){
		let that = this;
		let url = "http://localhost/api/product/read_paging.php?page=" + idx;//"http://www.androidbegin.com/tutorial/jsonparsetutorial.txt";//
		
		fetch(url)
		.then(response => response.json())
		.then(responseJson => {
			console.log(responseJson.paging.pages);
			that.setState({json : responseJson.records,paging:responseJson.paging.pages});
		})
		.catch(error => {
			console.error(error);
		});
	}
	
  render(){
	var data = this.state.json;
	var paging = this.state.paging;
	return (
    <div>
		<h1>Learning</h1>

		<h2>Start Again...</h2>
		<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="red" d="M22 9.24l-7.19-.62L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27 18.18 21l-1.63-7.03L22 9.24zM12 15.4l-3.76 2.27 1-4.28-3.32-2.88 4.38-.38L12 6.1l1.71 4.04 4.38.38-3.32 2.88 1 4.28L12 15.4z"/></svg>								
		
			
		<div className="col-lg-12 col-md-12 col-sm-12 col-xs-12">
		{
			 Object.keys(data).map((content, idx) => {
				return <div className="col-lg-3 col-md-4 col-sm-6 col-xs-12" onClick={() => this.onClickDetail(idx)}>
					<div className="box">
						{idx+1}. {data[idx].name}
						<p><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="red" d="M22 9.24l-7.19-.62L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27 18.18 21l-1.63-7.03L22 9.24zM12 15.4l-3.76 2.27 1-4.28-3.32-2.88 4.38-.38L12 6.1l1.71 4.04 4.38.38-3.32 2.88 1 4.28L12 15.4z"/></svg>								
						</p>
					</div>
				</div>
			}) 
		}
		</div>
		<div className="col-lg-12 col-md-12 col-sm-12 col-xs-12 text-center">
		{
			Object.keys(paging).map((page, indx) => {
				return <span className={'page '+ paging[indx].current_page} onClick={()=>this.pagination(paging[indx].page)}>
					{paging[indx].page}
				</span>
			})
		}
		</div>
	  <div className="test">
            
      </div>
		<Listitem value="{data}"></Listitem>
      <ol>
        <li>Review the <Link to="/fuel-savings">Fuel saving</Link></li>
        <li>Remove the demo and start coding: npm run remove-demo</li>
      </ol>
    </div>
  );
  }
}


function getMoviesFromApiAsync() {
  return fetch('https://facebook.github.io/react-native/movies.json')
    .then(response => response.json())
    .then(responseJson => {
      return responseJson.movies;
    })
    .catch(error => {
      console.error(error);
    });
}
const PlacePage1 = () => {
	
  return (
    <div>
      <h1>Learning</h1>

      <h2>Start Again...</h2>
      <ol>
        <li>Review the <Link to="/fuel-savings">Fuel saving</Link></li>
        <li>Remove the demo and start coding: npm run remove-demo</li>
      </ol>
    </div>
  );
};

//export default PlacePage;
