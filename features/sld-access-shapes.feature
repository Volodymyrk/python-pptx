Feature: Access shapes on a slide
  In order to operate on a shape in a slide
  As a developer using python-pptx
  I need a shape collection to provide access to shapes on a slide

  @wip
  Scenario: Access shape collection
     Given a slide having two shapes
      Then I can access the shape collection of the slide
       And the length of the shape collection is 2

  @wip
  Scenario: Access shape in shape collection
     Given a shape collection containing two shapes
      Then I can iterate over the shapes
       And I can access a shape by index
