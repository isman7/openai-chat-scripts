/*
## Firebase Cloud Function to delete collections 

This script was generated playing with https://chat.openai.com/chat, and it might not be functional, but it seems to me it is. It follows some logic implemented in bicidata/bicidata. 

> 3 minutes

### Prompts: 

- Hi there, could you explain me this code? (paste the code in https://github.com/bicidata/bicidata/blob/feature/create-process-datasets/apps/api/functions/index.js) 
- And this one? (https://raw.githubusercontent.com/isman7/openai-chat-scripts/master/firebase_gbfs_clean_snapshots.js)
- I want a similar function related to this later one. I want to access all the snapshots present in the collection of the day before, and then store them in cloud storage. How could you modify the example to do so?

*/

// The Cloud Functions for Firebase SDK to create Cloud Functions and setup triggers.
const functions = require("firebase-functions");

// The Firebase Admin SDK to access Firestore and Cloud Storage.
const admin = require('firebase-admin');
admin.initializeApp();

// A function to access and store old GBFS snapshots:
exports.gbfsStoreSnapshots = functions
    // .region('europe-west1')  // TODO changing region brakes the firebase "rewrite" rule.
    .pubsub.schedule('0 2 * * *')  // Run at 2:00 AM UTC0 every day.
    .onRun(async (context) => {
        let yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);

        let year = yesterday.getFullYear().toString();
        let month = (yesterday.getMonth() + 1).toString().padStart(2, "0");
        let day = yesterday.getDate().toString().padStart(2, "0");

        let collectionToAccess = `snapshots_${year}-${month}-${day}`;

        // Access the collection of snapshots from the day before.
        let snapshotQuery = await admin.firestore().collection(collectionToAccess).get();

        // Iterate over the snapshots and store them in Cloud Storage.
        snapshotQuery.forEach(async snapshot => {
            let fileName = `${snapshot.id}.json`;
            let file = bucket.file(fileName);

            // Store the snapshot in Cloud Storage.
            await file.save(JSON.stringify(snapshot.data()));

            functions.logger.info(`Successfully stored snapshot ${fileName} in Cloud Storage.`, {structuredData: true});
        });

        return null;
    });

