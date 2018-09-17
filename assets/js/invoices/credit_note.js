import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import $ from 'jquery';

export default class CreditNoteTable extends Component{
    constructor(props){
        super(props);
        this.state = {
            elements : [],
            credit: {}
        }
    }
    componentDidMount() {
        //prepopulate the form
        let decomposedURL = window.location.href.split('/');
        let pk = decomposedURL[decomposedURL.length - 1]; 
        axios({
            url: '/invoicing/api/sales-invoice/' + pk,
            data: {},
            method: 'GET'
        }).then(res => {
            let credits = {};
            let i = 0;
            console.log(res.data);
            for( i in res.data.salesinvoiceline_set){
                credits[res.data.salesinvoiceline_set[i].id] = 0.0;
            }
            this.setState({
                elements: res.data.salesinvoiceline_set,
                credit: credits
            });
            
        });

        // place hidden input 
        /*
        document.getElementsByTagName('form')
            .appendChild()
            .document.createElement('input').a
        */
        $('<input>').attr({
            'name': 'returned-items',
            'type': 'hidden',
            'value': '',
            'id': 'id-returned-items'
        }).appendTo('form');
    }
        
    
    handleInputChange(data){
        let newCreditValues = this.state.credit;
        newCreditValues[data.id] = data.returned;
        this.setState({
            credit: newCreditValues
        });
        let inputVal = encodeURIComponent(
            JSON.stringify(this.state.credit));
        $('#id-returned-items').val(inputVal);
    }
    
    render(){
        return(
            <table className="table">
                <thead className="bg-primary text-white">
                    <tr>
                    <th>Ordered Qty</th>
                    <th>Description</th>
                    <th>Price</th>
                    <th>Returned</th>
                    <th>Credit</th>
                    </tr>
                </thead>
                <tbody>
                    {this.state.elements.map((element, i) =>(
                        <CreditNoteLine key={i} 
                            element={element}
                            returnHandler={this.handleInputChange.bind(this)} />
                        
                    ))}
                    
                </tbody>
            </table>
        )
    }
}

class CreditNoteLine extends Component{
    constructor(props){
        super(props);
        this.state = {
            credit: 0.0,
            returned: 0.0,
            id: ""
        }
    }
    handleInputChange(evt){
        let credit = this.props.element.product.unit_sales_price * evt.target.value;
        this.setState({
            returned: evt.target.value,
            id: this.props.element.id,
            credit: credit
        }, () => {
            this.props.returnHandler(this.state)
        });
        
    }
    render(){
        return(
        <tr>
            <td>{this.props.element.quantity}</td>
            <td>{this.props.element.product.name}</td>
            <td>{this.props.element.product.unit_sales_price.toFixed(2)}</td>
            <td>
                <input type="number" 
                    name = {this.props.element.id}
                    onChange={this.handleInputChange.bind(this)}
                    className="form-control"/>
            </td>
            <td>{this.state.credit.toFixed(2)}</td>
        </tr>);
    }
}