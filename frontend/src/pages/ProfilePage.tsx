import { useSession } from '@/hooks/SessionContext';
import { useUser, useTasteProfile } from '@/services/queries';
import { ProfileSummary } from '@/components/ProfileSummary';
import { TasteDimensionCard } from '@/components/TasteDimensionCard';
import { TasteProfileSkeleton } from '@/components/TasteProfileSkeleton';
import { ErrorState } from '@/components/ErrorState';
import { ArrowLeft, RotateCcw } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export function ProfilePage() {
  const { userId } = useSession();
  const navigate = useNavigate();

  const { data: user, isLoading: isUserLoading, isError: isUserError } = useUser(userId);
  const { data: profile, isLoading: isProfileLoading, isError: isProfileError } = useTasteProfile(userId);

  if (isUserLoading || isProfileLoading) {
    return <TasteProfileSkeleton />;
  }

  if (isUserError || isProfileError || !user || !profile) {
    return <ErrorState message="Failed to load your Taste Identity profile." onRetry={() => navigate('/quiz')} />;
  }

  const dimensions = [
    { label: 'spice', value: profile.spice_preference },
    { label: 'saltiness', value: profile.saltiness_preference },
    { label: 'sweetness', value: profile.sweetness_preference },
    { label: 'tanginess', value: profile.tanginess_preference },
    { label: 'creaminess', value: profile.creaminess_preference },
    { label: 'oiliness', value: profile.oiliness_preference },
    { label: 'masala_intensity', value: profile.masala_intensity_preference },
    { label: 'crunch', value: profile.crunchiness_preference },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-background pb-12">
      {/* Top Bar */}
      <div className="sticky top-0 z-30 flex items-center justify-between p-4 bg-background/80 backdrop-blur border-b border-border">
        <button
          onClick={() => navigate('/restaurant')}
          className="p-2 rounded-full hover:bg-muted transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <h1 className="text-base font-bold">Your Taste Identity</h1>
        <div className="w-9" />
      </div>

      <main className="flex-1 max-w-3xl mx-auto w-full p-4 md:p-6 space-y-6">
        <ProfileSummary user={user} profile={profile} />

        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-bold">Your Flavor Vectors</h3>
            <button
              onClick={() => navigate('/quiz')}
              className="flex items-center gap-1.5 text-xs font-bold text-primary hover:underline"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Retake Quiz</span>
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {dimensions.map((dim) => (
              <TasteDimensionCard key={dim.label} label={dim.label} value={dim.value} />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
