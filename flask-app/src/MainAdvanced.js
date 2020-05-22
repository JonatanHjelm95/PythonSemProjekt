import React, { Component } from 'react';
import facade from './apiFacade'
import Loader from './Loader'

class MainAdvanced extends Component {
    constructor(props) {
        super(props);
        this.state = {
            name: 'Google',
            type: 'STOCK',
            method: 'LR',
            n: 30,
            gammaType: 'auto',
            gamma: 1.0,
            kernel: 'rbf',
            image: '',
            loading: false,
            error: ''
        }
    }


    async doFetch(name, type, method, n, gamma, kernel, gammaType) {
        this.setState({
            loading: true,
            error: ''
        })
        name = name.replace(' ', '+')
        console.log(name, type)
        if (gammaType != 'specific') {
            gamma = gammaType
        }
        var json = await facade.advancedPredict(name, type, method, n, gamma, kernel)
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
    changeAmount(evt) {
        evt.persist()
        var n = evt.target.value
        this.setState({
            n: n
        })
    }
    changeMethod(evt) {
        evt.persist()
        var method = evt.target.value
        this.setState({
            method: method
        })
    }
    changeKernel(evt) {
        evt.persist()
        var kernel = evt.target.value
        this.setState({
            kernel: kernel
        })
    }
    changeGamma(evt) {
        evt.persist()
        var gamma = evt.target.value
        this.setState({
            gamma: gamma
        })
    }
    changeGammaType(evt) {
        evt.persist()
        var type = evt.target.value
        this.setState({
            gammaType: type
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
                        <form>

                            <input onChange={this.onChange} className="nameInput" type="text" id="name" defaultValue='Google'
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
                    <div className="type-input-container">
                        <select className="Method" onChange={(evt) => this.changeMethod(evt)}>
                            <option value="LR">Linear Regression</option>
                            <option value="SVM">Support Vector Regression</option>
                        </select>
                        <input
                            onChange={(evt) => this.changeAmount(evt)}
                            type="number"
                            step="1"
                            min='30'
                            defaultValue={30}
                        ></input>
                    </div>

                    {this.state.method == 'SVM' ? (<div>
                        <div className="type-input-container">
                            <select className="Kernel" onChange={(evt) => this.changeKernel(evt)}>
                                <option value="rbf">RBF</option>
                                <option value="linear">Linear</option>
                                <option value="poly">Poly</option>
                                <option value="sigmoid">Sigmoid</option>
                                <option value="precomputed">Precomputed</option>
                            </select>
                        </div>

                        <div className="type-input-container">
                            <select className="Gamma" onChange={(evt) => this.changeGammaType(evt)}>
                                <option value="auto">Auto</option>
                                <option value="scale">Scale</option>
                                <option value="specific">Specific...</option>
                            </select></div>
                        {this.state.gammaType == 'specific' ? (<div><input
                            onChange={(evt) => this.changeGamma(evt)}
                            type="number"
                            step="0.001"
                            min='0'
                            max='1' defaultValue={1.0}
                        ></input></div>) : (<div></div>)}
                    </div>
                    ) : (
                            <div></div>
                        )}

                    <button onClick={(evt) => this.doFetch(this.state.name, this.state.type, this.state.method, this.state.n, this.state.gamma, this.state.kernel, this.state.gammaType)}
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
export default MainAdvanced;