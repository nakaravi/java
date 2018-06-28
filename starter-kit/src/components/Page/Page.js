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
import s from './Page.css';

import httpRequest from '../../components/Helper/httpRequest';

class Page extends React.Component {
	static propTypes = {
		title: PropTypes.string.isRequired,
		html: PropTypes.string.isRequired,
		data:{},
		
	};
	constructor(props) {
        super(props);
		this.state = {
            data: [],
        };
    }
	componentDidMount() {
		var d = httpRequest.get('http://localhost/api/product/read.php').then(res =>this.setState({data:res.records}));
	}
	

  render() {
    const { title, html } = this.props;
    return (
      <div className={s.root}>
        <div className={s.container}>
          <h1>{title}</h1>
		  
		  {this.state.data.map(item => (
            <article key={item.id} className={s.newsItem}>
              <h3 className={s.newsTitle}>
                <a href={item.link}>{item.name}</a>
              </h3>
			  <div>
				{item.description}
			  </div>
              <div
                className={s.newsDesc}
                // eslint-disable-next-line react/no-danger
                dangerouslySetInnerHTML={{ __html: item.content }}
              />
            </article>
          ))}
		  
          <div
            // eslint-disable-next-line react/no-danger
            dangerouslySetInnerHTML={{ __html: html }}
          />
        </div>
      </div>
    );
  }
}

export default withStyles(s)(Page);
