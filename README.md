# PysalNBGallery

Update gallery with the following steps:
<li> Save a screenshot of the notebook in the images folder </li>
<li> Add the image, link, and description to the appropriate category in index.html </li>

For example, if I'd like to add a new notebook to the Spatial Dynamics section, insert here:

    <div class='container-fluid'>
    <div class="jumbotron">
      <div class='row'></div>
      <h2  align="left">Space-Time Analysis</h2> <br>
      <div class='row'>
    <div class='col-md-6'>
     <a href="https://github.com/sjsrey/aerus2015/blob/master/esda/12_spatial_dynamics.ipynb">
     <img src="images/dynamics.png"style="height:300px;"> </a><br><br>
     <p> Spatial Dynamics. </p>
   </div>

   // Add this section here:
   <div class='col-md-6'>
     <a href="LINK TO YOUR NOTEBOOK HERE">
     <img src="images/LINK TO IMAGE HERE"style="height:300px;"> </a><br><br>
     <p> DESCRIPTION OF YOUR NOTEBOOK HERE. </p>
   </div>
   // End of new section

	</div> 
  </div>
  </div>