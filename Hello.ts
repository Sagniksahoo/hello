generateJSON(): Blob {
    // Construct the JSON object
    const jsonData = {
      towerName: this.formData.towerName || '',
      Submitter_email_id: this.formData.Submitter_email_id || '',
      subscriptionName: this.formData.subscriptionName || '',
      region: this.formData.region || '',
      ApplicationName: this.formData.ApplicationName || '',
      environment: this.formData.environment || '',
      ownerNameEmail: this.formData.ownerNameEmail || '',
      supportTeamEmail: this.formData.supportTeamEmail || '',
      developmentTeamEmail: this.formData.developmentTeamEmail || '',
      technicalDesignDocument: this.formData.tdd || '',
      alertActionGroup: this.formData.alertActionGroup || '',
      tags: this.formData.tags || '',
      nsgRules: this.nsgRules,
      resources: this.addedResources.map(resource => {
        const parametersObject = resource.parameters.reduce((acc, param) => {
          acc[param.label] = param.type === 'checkbox' 
            ? this.getCheckboxValues(param) 
            : param.value || ''; // Map label to its actual value
          return acc;
        }, {}); // Accumulate as a key-value pair object

        return {
          name: resource.name,
          parameters: parametersObject, // Use the transformed object
        };
      }),
    };

    // Convert JSON object to string
    const jsonString = JSON.stringify(jsonData, null, 2);

    // Create a Blob from the JSON string
    const blob = new Blob([jsonString], { type: 'application/json' });

    // Create a download link
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');

    // Construct the filename for the JSON
    const jsonFilename = `${this.formData.Submitter_email_id}-${this.formData.towerName}-${this.formData.ApplicationName}-${this.getFormattedDate()}.json`;

    a.href = url;
    a.download = jsonFilename; // Set the filename

    // Programmatically click the link to trigger the download
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    return blob; // Return the Blob
}
