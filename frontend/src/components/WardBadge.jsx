const wardColors = {
  'general_ward': 'bg-green-100 text-green-800',
  'emergency_ward': 'bg-red-100 text-red-800',
  'mental_health_ward': 'bg-purple-100 text-purple-800',
};

export default function WardBadge({ ward }) {
  const friendlyName = ward.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
  const colorClass = wardColors[ward] || 'bg-gray-100 text-gray-800';

  return (
    <span className={`inline-block px-4 py-2 rounded-full font-semibold text-sm mb-4 ${colorClass}`}>
      Ward: {friendlyName}
    </span>
  );
}