import React, { Component } from 'react';
import facade from './apiFacade'
import Loader from './Loader'

class Main extends Component {
    constructor(props) {
        super(props);
        this.state = {
            name: 'Google',
            type: 'STOCK',
            image: '',
            loading: false,
            error: ''
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
        this.setState({
            loading: true,
            error: ''
        })
        name = name.replace(' ', '+')
        console.log(name, type)
        var json = await facade.predict(name, type)
        var encodedData = await json.graph
        if (encodedData != null) {
            encodedData = encodedData.toString().replace('b\'', '').replace('\'', '')
            this.createImageFromB64(encodedData)
        } else {
            this.setState({
                error: json.error
            })
        }
        this.setState({
            loading: false
        })
        //graph = graph.toString().replace('b\'','')
        //graph = base64.decode(graph)
        //await console.log(json)
        //console.log(graph)
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

    createImageFromB64(encodedData) {
        var image = 'data:image/png[jpg];base64, ' + encodedData
        this.setState({
            image: image
        })
    }


    render() {

        return (
            <div>
                
                <div>
                    <div className="name-input-container">
                        <form onChange={this.onChange}>
                            <input className="nameInput" type="text" id="name" defaultValue='Google'
                            />
                        </form>
                    </div>
                    <div className="type-input-container">
                        <select className="Type" onChange={(evt) => this.changeType(evt)}>
                            <option value="STOCK">Stock</option>
                            <option value="FOREX">Forex</option>
                            <option value="CRYPTO">Crypto Currency</option>
                        </select>
                    </div>
                    <button onClick={(evt) => this.doFetch(this.state.name, this.state.type)}
                    >Predict</button>
                </div>
                <div>
                    {this.state.loading ? (<div className="loader-container"><Loader /></div>) : (<img src={this.state.image} style={{ width: window.innerWidth, height: 'auto' }} />)}
                    {this.state.error.length > 0 ? (<h1>{this.state.error}</h1>) : (<div></div>)}
                </div>
            </div>
        );
    }
}
export default Main;