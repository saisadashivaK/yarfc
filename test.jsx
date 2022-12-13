
        import React, { useState } from 'react';


        function Component(props)
        {
            const [$formState, $setFormState] = useState({"name": "", "dob": "", "contact_number": "", "class_10_status": false, "address_line_1": "", "address_line_2": "", "address_line_3": ""});
            const [$formValidState, $setFormValidState] = useState($defaultValidityState);
            
            const $formStateHandler = (stateName) => (e) => {
                const value = e.target.type === "checkbox" ? e.target.checked : e.target.value;
                $setFormState({
                    ...$formState,
                    [stateName]: value
                });
            };
            
            
            return (
              <div className="form-container">
	<div className="form-row">
		<div className="input-group">
			<label for="name">Name</label>
			<input type="text" name="name" id="name" placeholder="" value=$formState.{name} onChange={formStateHandler} />
		{ $formStateValid.name ? (<p className="error"></p>): (<p></p>)}
		</div>
	</div>
	<div className="form-row">
		<div className="input-group">
			<label for="dob">Date of Birth</label>
			<input type="date" name="dob" id="dob" value=$formState.{dob} onChange={formStateHandler} />
		{ $formStateValid.dob ? (<p className="error"></p>): (<p></p>)}
		</div>
	</div>
	<div className="form-row">
		<div className="input-group">
			<label for="contact_number">Contact Number</label>
			<input type="tel" name="contact_number" id="contact_number" placeholder="" value=$formState.{contact_number} onChange={formStateHandler} />
		{ $formStateValid.contact_number ? (<p className="error"></p>): (<p></p>)}
		</div>
			<label for="class_10_status">Class 10th status</label>
			<input type="checkbox" name="class_10_status" id="class_10_status" value=$formState.{class_10_status} onChange={formStateHandler} />
	</div>
	<div className="form-row">
		<div className="input-group">
			<label for="address_line_1">Address line 1</label>
			<input type="text" name="address_line_1" id="address_line_1" placeholder="" value=$formState.{address_line_1} onChange={formStateHandler} />
		{ $formStateValid.address_line_1 ? (<p className="error"></p>): (<p></p>)}
		</div>
	</div>
	<div className="form-row">
		<div className="input-group">
			<label for="address_line_2">Address line 2</label>
			<input type="text" name="address_line_2" id="address_line_2" placeholder="" value=$formState.{address_line_2} onChange={formStateHandler} />
		{ $formStateValid.address_line_2 ? (<p className="error"></p>): (<p></p>)}
		</div>
	</div>
	<div className="form-row">
		<div className="input-group">
			<label for="address_line_3">Address line 3</label>
			<input type="text" name="address_line_3" id="address_line_3" placeholder="" value=$formState.{address_line_3} onChange={formStateHandler} />
		{ $formStateValid.address_line_3 ? (<p className="error"></p>): (<p></p>)}
		</div>
	</div>
</div>
  
            );
            
            
            
        }
        