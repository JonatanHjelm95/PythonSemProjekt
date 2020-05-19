import React, { Component } from 'react';
import facade from './apiFacade'

class Main extends Component {
    constructor(props) {
        super(props);
        this.state = {
            name: 'Google',
            type: 'STOCK'
        }
    }
    async componentDidMount() {
        this.mounted = true;
        /* if(this.mounted){
            
        } */

    }
    componentWillUnmount() {
        this.mounted = false;
    }

    async doFetch(name, type) {
        name = name.replace(' ','+')
        console.log(name, type)
        var json = await facade.predict(name, type)
        await console.log(json)

    }

    onChange = evt => {
        evt.persist();
        this.setState({
            [evt.target.id]: evt.target.value,
        })
    };

    changeType(evt) {
        evt.persist()
        var type = evt.target.value
        this.setState({
            type: type
        })
    }


    render() {
        
        return (
            <div>
            <div>
                <div className="name-input-container">
                                    <form onChange={this.onChange}>
                                        <input className="nameInput" type="text" id="name" defaultValue='Google' />
                                    </form>
                                </div>
                <div className="type-input-container">
                    <select className="Type" onChange={(evt) => this.changeType(evt)}>
                        <option value="STOCK">Stock</option>
                        <option value="FOREX">Forex</option>
                        <option value="CRYPTO">Crypto Currency</option>
                    </select>
                </div>
                <button onClick={(evt) => this.doFetch(this.state.name, this.state.type)}>Go</button>
            </div>
            <img src={require('./figure.png')} alt="chart"></img>

            </div>
        );
    }
}
export default Main;