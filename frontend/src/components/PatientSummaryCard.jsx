export default function PatientSummaryCard({ name, age, query, ward }) {
  const friendlyWard = ward.replace('_', ' ');
  return (
    <div className="w-full max-w-md bg-white border border-gray-200 rounded-lg shadow p-6 mb-4">
      <h2 className="text-xl font-bold text-gray-800 mb-2">Patient Summary</h2>
      <div className="space-y-2 text-sm text-gray-600">
        <p><span className="font-medium">Name:</span> {name}</p>
        <p><span className="font-medium">Age:</span> {age}</p>
        <p><span className="font-medium">Main Query:</span> {query}</p>
        <p><span className="font-medium">Ward:</span> {friendlyWard}</p>
      </div>
    </div>
  );
}