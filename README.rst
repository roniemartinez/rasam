

.. raw:: html

   <table>
       <tr>
           <td>License</td>
           <td><img src='https://img.shields.io/pypi/l/rasam.svg?style=for-the-badge' alt="License"></td>
           <td>Version</td>
           <td><img src='https://img.shields.io/pypi/v/rasam.svg?logo=pypi&style=for-the-badge' alt="Version"></td>
       </tr>
       <tr>
           <td>Github Actions</td>
           <td><img src='https://img.shields.io/github/workflow/status/roniemartinez/rasam/Python?label=actions&logo=github%20actions&style=for-the-badge' alt="Github Actions"></td>
           <td>Coverage</td>
           <td><img src='https://img.shields.io/codecov/c/github/roniemartinez/rasam/branch?label=codecov&logo=codecov&style=for-the-badge' alt="CodeCov"></td>
       </tr>
       <tr>
           <td>Supported versions</td>
           <td><img src='https://img.shields.io/pypi/pyversions/rasam.svg?logo=python&style=for-the-badge' alt="Python Versions"></td>
           <td>Wheel</td>
           <td><img src='https://img.shields.io/pypi/wheel/rasam.svg?style=for-the-badge' alt="Wheel"></td>
       </tr>
       <tr>
           <td>Status</td>
           <td><img src='https://img.shields.io/pypi/status/rasam.svg?style=for-the-badge' alt="Status"></td>
           <td>Downloads</td>
           <td><img src='https://img.shields.io/pypi/dm/rasam.svg?style=for-the-badge' alt="Downloads"></td>
       </tr>
   </table>


rasam
=====

Rasa Improved

Usage
-----

Installation
^^^^^^^^^^^^

.. code-block:: bash

   pip install rasam

Rasa ``config.yml``
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

   importers:
     - name: rasam.PlaceholderImporter
       fake_data_count: 10  # default value is 1

   pipeline:
     - name: rasam.RegexEntityExtractor
     - name: rasam.URLEntityExtractor

Rasa ``nlu.yml``
^^^^^^^^^^^^^^^^^^^^

PlaceholderImporter
~~~~~~~~~~~~~~~~~~~

The ``PlaceholderImporter`` removes the need to write unnecessary information (eg. name, address, numbers, etc.) and helps focus on writing test data.

Using ``{}`` placeholder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   nlu:
   - intent: tell_name
     examples: |
       - My name is {name}
       - I am {name} and he is {name}

Using ``@`` placeholder
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   nlu:
   - intent: tell_address
     examples: |
       - I live in @address
       - I stay at @address and @address

Mixing ``{}`` and ``@`` placeholders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to mix both ``{}`` and ``@`` placeholders but it is recommended to use only one style for consistency.

Available placeholders
~~~~~~~~~~~~~~~~~~~~~~


* any (if you need just any data)    
* integer    
* decimal    
* number     
* name       
* first_name 
* last_name  
* text       
* word       
* paragraph  
* uri        
* url        
* local_uri  
* email      
* date         
* time         
* month        
* day          
* timezone     
* company      
* license_plate
* address
* city
* country
* user_agent
* password
* user_name
* file_path

Rasam decorators
^^^^^^^^^^^^^^^^

Rasa relies too heavily on classes to define objects like actions, forms, etc. 
Rasam aims to remove these Rasa boilerplates to make writing chatbots easier.

@action decorator
~~~~~~~~~~~~~~~~~

The ``@action`` decorator converts function into an Action class. 
Here is an example of how we can write custom classes in Rasa:

.. code-block:: python

   class ActionHelloWorld(Action):

       def name(self) -> Text:
           return "action_hello_world"

       def run(self, dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

           dispatcher.utter_message(text="Hello World!")

           return []

The above code can be simplified using Rasam's ``@action`` decorator.

.. code-block:: python

   from rasam import action


   @action
   def action_hello_world(
       self: Action, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
   ) -> List[Dict[Text, Any]]:
       dispatcher.utter_message(text="Hello World!")
       return []

Author
------


* `Ronie Martinez <mailto:ronmarti18@gmail.com>`_
