/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-present Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import React from 'react';
import PropTypes from 'prop-types';
import withStyles from 'isomorphic-style-loader/lib/withStyles';
import s from './Stage.css';

import httpRequest from '../../components/Helper/httpRequest';

class Stage extends React.Component {
	constructor(props){
		super(props);
		this.loadHtml = this.loadHtml.bind(this);
		this.state = {
            data: [],
        };
	}
	
  static propTypes = {
    title: PropTypes.string.isRequired,
  };
  
  loadHtml=(arg, event)=>{
	var d = httpRequest.getHtml('/stage/stage.html').then(res =>{
		this.setState({data:res})
	});
	
  }

  render() {
    return (
      <div className={s.root}>
        <div className={s.container}>
          <h1>{this.props.title}</h1>
		  <button onClick={(e)=>this.loadHtml(1, e)} >add</button> 
          <div id="stage" ref="stage" className={s.stage} dangerouslySetInnerHTML={{__html: this.state.data}}></div>
        </div>
      </div>
    );
  }
}

export default withStyles(s)(Stage);
