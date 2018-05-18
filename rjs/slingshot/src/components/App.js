/* eslint-disable import/no-named-as-default */
import React from 'react';
import PropTypes from 'prop-types';
import { Switch, NavLink, Route } from 'react-router-dom';

import Header from './Header';
import HomePage from './HomePage';
import PlacePage from './PlacePage';
import FuelSavingsPage from '../containers/FuelSavingsPage';
import AboutPage from './AboutPage';
import NotFoundPage from './NotFoundPage';
import PlaceDetail from './PlaceDetail';


// This is a class-based component because the current
// version of hot reloading won't hot reload a stateless
// component at the top-level.
/* function getComponent(){console.log('ssssssssssssssssssss');
		var ele = document.getElementsByClassName('aside.side-bar');//.removeClass('collapse').addClass('expand');
		ele.className = 'side-bar expand';
	}; */
class App extends React.Component {

	constructor(props){
		super(props);
        this.state = {classToSend: true };
	}
	
	onClickHandler(){
        let ele = document.getElementById('sideNavigation');
		if(ele.className == 'side-bar shrink'){
			ele.className = 'side-bar expand';
		}else{
			ele.className = 'side-bar shrink';
		}
		
    }

  render() {
    const activeStyle = { color: 'blue' };
	
    return (
		<div>
			<header>
				<Header />
			</header>
			<div className="content">
				<aside id="sideNavigation" className="side-bar shrink">
					<div className="aside-navigation pointer" onClick={() => this.onClickHandler()} />
					<NavLink exact to="/" activeStyle={activeStyle}><span>Home</span></NavLink>
					<NavLink exact to="/places" activeStyle={activeStyle}><span>Places</span></NavLink>			  
					<NavLink to="/fuel-savings" activeStyle={activeStyle}><span>Demo App</span></NavLink>			  
					<NavLink to="/about" activeStyle={activeStyle}><span>About</span></NavLink>
				</aside>
				<div className="content-container">
					<Switch>
						<Route exact path="/" component={HomePage} />
						<Route path="/places" component={PlacePage} />
						<Route path="/detail/:id" component={PlaceDetail} />
						<Route path="/fuel-savings" component={FuelSavingsPage} />
						<Route path="/about" component={AboutPage} />
						<Route component={NotFoundPage} />
					</Switch>
				</div>
			</div>
			
			<footer className="text-center">
				Footer section
			</footer>
		</div>
    );
  }
}

App.propTypes = {
  children: PropTypes.element
};

export default App;
