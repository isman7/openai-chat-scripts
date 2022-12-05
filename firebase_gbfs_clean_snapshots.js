/*
## Firebase Cloud Function to delete collections 

This script was generated playing with https://chat.openai.com/chat, and it might not be functional, but it seems to me it is. It follows some logic implemented in bicidata/bicidata. 

> 3 minutes

### Prompts: 

- Hi! Could you please explain me what this Python code does? (paste the code in https://github.com/bicidata/bicidata/blob/feature/create-process-datasets/scripts/script.py ) 
- And this one? (paste the code in https://github.com/bicidata/bicidata/blob/feature/create-process-datasets/apps/api/functions/index.js) 


*/

// The Cloud Functions for Firebase SDK to create Cloud Functions and setup triggers.
const functions = require("firebase-functions");

// The Firebase Admin SDK to access Firestore.
const admin = require('firebase-admin');
admin.initializeApp();

// A function to clean up old GBFS snapshots:
exports.gbfsCleanSnapshots = functions
    // .region('europe-west1')  // TODO changing region brakes the firebase "rewrite" rule.
    .pubsub.schedule('0 2 * * *')  // Run at 2:00 AM UTC0 every day.
    .onRun(async (context) => {
        let threeDaysAgo = new Date();
        threeDaysAgo.setDate(threeDaysAgo.getDate() - 3);

        let year = threeDaysAgo.getFullYear().toString();
        let month = (threeDaysAgo.getMonth() + 1).toString().padStart(2, "0");
        let day = threeDaysAgo.getDate().toString().padStart(2, "0");

        let collectionToDelete = `snapshots_${year}-${month}-${day}`;

        // Delete the collection of snapshots from three days ago.
        let deleteResult = await admin.firestore().collection(collectionToDelete).delete();

        functions.logger.info(`Successfully deleted collection ${collectionToDelete}.`, {structuredData: true});

        return null;
    });
