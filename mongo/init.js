const fs = require('fs');
const path = require('path');

const db = connect("localhost:27017/School_Timetable");

const collections = {
    "class_timetable": "Class_Timetable",
    "room_timetable": "Room_Timetable"
};

for (const collectionKey in collections) {
    const collectionName = collections[collectionKey];
    const filePath = path.join('/docker-entrypoint-initdb.d/output_json', `${collectionKey}.json`);
    
    if (fs.existsSync(filePath)) {
        const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        db[collectionName].insertMany(data);
        print(`Inserted ${data.length} documents into ${collectionName}`);
    } else {
        print(`File not found: ${filePath}`);
    }
}
