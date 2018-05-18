import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import renderHTML from 'react-render-html';
import Button from 'material-ui/Button';

export default class PlaceDetail extends React.Component{

	constructor(props){
		super(props);
		this.state = {
			id:this.props.match.params.id,
			json:[],
			tabIndex: 0
		};
	}
	
	getInitialState() {
		return {
		  json: Map({ title: 0 })
		}
	}
	  
	componentDidMount() {
		
		let that = this;
		let id = that.props.match.params.id;
		let url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22nome%2C%20ak%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys";
		console.log(url);
		fetch(url)
		.then(response => response.json())
		.then(responseJson => {
			that.setState({json : responseJson.query.results.channel});
			that.json = responseJson.query.results.channel;
		})
		.catch(error => {
			console.error(error);
		});
	}

	displayTable(data){
		const items = Object.keys(data).map((content, key) => {
			<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
				{data[key].code}
			</div>
		});
		return items;
		
	}
		
	render(){
		var data = this.state.json;
		
		var bannerStyle = {
            background: 'url(' + ((!data||data.length<=0)?'../images/logo.png':data.image.url) + ') 0/100% 100% no-repeat',
            backgroundSize: '0/100% 100%',
            backgroundPosition: 'center',
        }
		return(
			!data||data.length<=0?<div>Loading...</div>:
			<div>
				<h3>{data.title}</h3>
				<div className="col-lg-12 col-md-12 col-sm-12 col-xs-12">
					<div className="col-lg-5 col-md-5 col-sm-6 col-xs-12 padding-all-20">
						<div className="img-box" style={bannerStyle}>
							
						</div>
					</div>
					<div className="col-lg-7 col-md-7 col-sm-6 col-xs-12">
						<Button raised color="primary">
						  Hello World
						</Button>
					</div>
				</div>
				<div className="col-lg-12 col-md-12 col-sm-12 col-xs-12" >
					{renderHTML(data.item.description)}
				</div>
				<div className="col-lg-12 col-md-12 col-sm-12 col-xs-12">
					<Tabs selectedIndex={this.state.tabIndex} onSelect={tabIndex => this.setState({tabIndex})}>
						<TabList>
						  <Tab>forecast</Tab>
						  <Tab>Title 2</Tab>
						  <Tab>Title 3</Tab>
						  <Tab>Title 4</Tab>
						</TabList>
					 
						<TabPanel>
						  <div className="row padding-all-10 bold heading">
									<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
										Code
									</div>
									<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
										Date
									</div>
									<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
										Day
									</div>
									<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
										High
									</div>
									<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
										Low
									</div>
									<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
										Text
									</div>
								</div>
						  {
							Object.keys(data.item.forecast).map((content, key) => {
								return <div className="row">
									<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
										{data.item.forecast[key].code}
									</div>
									<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
										{data.item.forecast[key].date}
									</div>
									<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
										{data.item.forecast[key].day}
									</div>
									<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
										{data.item.forecast[key].high}
									</div>
									<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
										{data.item.forecast[key].low}
									</div>
									<div className="col-lg-2 col-md-2 col-sm-2 col-xs-2">
										{data.item.forecast[key].text}
									</div>
								</div>
							})
						  }
							
						  
						</TabPanel>
						<TabPanel>
						  <h2>Any content 2</h2>
						</TabPanel>
						<TabPanel>
						  <h2>Any content 133333333</h2>
						</TabPanel>
						<TabPanel>
						  <h2>Any content 2444444444444444</h2>
						</TabPanel>
					</Tabs>
				</div>
				<p>Title : {data.title}</p>
				<p>Release Year : {data.releaseYear}</p>
			</div>
		);
	};

}
