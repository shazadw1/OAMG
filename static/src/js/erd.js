/** @odoo-module **/
const {xml, Component} = owl;
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";

export class CustomMany2ManyField extends Component {
    constructor() {
        super(...arguments);
        const record = this.props.record;

        const json = record.data.json;

        // Parse JSON data
        this.models = json ? JSON.parse(json) : [];
    }

    showDetails(model) {
        alert(`Model Name: ${model.name}`);
    }
}

CustomMany2ManyField.template = xml`
    <div style="display: grid; grid-template-columns: repeat(4, 1fr);gap:40px">
        <t t-foreach="models" t-as="model" t-key="model.id || model.name" t-attf-class="container">
            <div t-if="model">
                <div style="min-width:250px; background-color:#ddd;">
                    <div style="border: 1px solid #333;display: flex;align-items: center;justify-content: center;padding: 5px">
                        <t t-esc="model.name"/>
                    </div>
                    <div style="margin-top: 0;padding: 10px">
                        <ul>
                            <li t-foreach="model.fields" t-as="field" t-key="field.id || field.name" style="display: flex; align-items: center; gap: 10px">
                                <p><t t-esc="field.name"/></p>
                                <p t-if="field.related_model"> <strong>(<t t-esc="field.related_model"/>)</strong></p>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </t>
    </div>
`;

CustomMany2ManyField.props = standardFieldProps;

registry.category("fields").add("custom_many2many_widget", CustomMany2ManyField);
