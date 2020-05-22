/* eslint-disable no-throw-literal */
//const URL = "http://localhost:5001";



class ApiFacade {
    //Insert utility-methods from a latter step (d) here
    makeOptions(method, addToken, body) {
        var opts = {
            method: method,
            headers: {
                "Content-type": "application/json",
                'Accept': 'application/json',
            }
        }
        if (body) {
            opts.body = JSON.stringify(body);
        }
        return opts;
    }

    predict = async (name, type) => {
        const options = this.makeOptions("POST", false, { name: name, type: type });
        const res = await fetch("/api/predict", options)
        const json = await res.json();
        if (!res.ok) {
            throw { status: res.status, fullError: json }
        }
        return json;
    }
    advancedPredict = async (name, type, method, n, gamma, kernel) => {
        const options = this.makeOptions("POST", false, { name: name, type: type, method: method, n: n, gamma: gamma, kernel:kernel});
        const res = await fetch("/api/predict/specific", options)
        const json = await res.json();
        if (!res.ok) {
            throw { status: res.status, fullError: json }
        }
        return json;
    }
}


const facade = new ApiFacade();

export default facade;
