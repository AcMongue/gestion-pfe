"""
Test complet de toutes les URLs du système
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import reverse, NoReverseMatch

def test_all_urls():
    """Tester que toutes les URLs importantes sont accessibles"""
    print("\n" + "="*80)
    print("TEST COMPLET DES URLs")
    print("="*80 + "\n")
    
    urls_to_test = {
        'Users': [
            ('users:register', {}),
            ('users:login', {}),
            ('users:logout', {}),
            ('users:dashboard', {}),
            ('users:profile', {}),
            ('users:profile_edit', {}),
            ('users:user_list', {}),
            ('users:user_detail', {'pk': 1}),
        ],
        'Subjects': [
            ('subjects:list', {}),
            ('subjects:subject_list', {}),
            ('subjects:create', {}),
            ('subjects:subject_create', {}),
            ('subjects:detail', {'pk': 1}),
            ('subjects:update', {'pk': 1}),
            ('subjects:subject_edit', {'pk': 1}),
            ('subjects:my_subjects', {}),
            ('subjects:my_applications', {}),
            ('subjects:apply', {'subject_pk': 1}),
            ('subjects:assignments_manage', {}),
        ],
        'Projects': [
            ('projects:list', {}),
            ('projects:project_list', {}),
            ('projects:create', {}),
            ('projects:project_create', {}),
            ('projects:my_projects', {}),
            ('projects:detail', {'pk': 1}),
            ('projects:update', {'pk': 1}),
            ('projects:milestone_create', {'project_pk': 1}),
            ('projects:deliverable_create', {'project_pk': 1}),
            ('projects:deliverable_submit', {'project_pk': 1}),
        ],
        'Communications': [
            ('communications:inbox', {}),
            ('communications:message_list', {}),
            ('communications:sent', {}),
            ('communications:compose', {}),
            ('communications:message_create', {}),
            ('communications:message_detail', {'pk': 1}),
            ('communications:notifications', {}),
            ('communications:notification_list', {}),
        ],
        'Defenses': [
            ('defenses:list', {}),
            ('defenses:defense_list', {}),
            ('defenses:calendar', {}),
            ('defenses:planning', {}),
            ('defenses:defense_planning', {}),
            ('defenses:detail', {'pk': 1}),
            ('defenses:create', {'project_id': 1}),
        ],
        'Archives': [
            ('archives:list', {}),
            ('archives:archive_list', {}),
            ('archives:detail', {'pk': 1}),
            ('archives:reports', {}),
            ('archives:generate_report', {}),
        ],
    }
    
    total_urls = 0
    successful_urls = 0
    failed_urls = []
    
    for category, urls in urls_to_test.items():
        print(f"\n{category}:")
        print("-" * 40)
        category_success = 0
        
        for url_name, kwargs in urls:
            total_urls += 1
            try:
                url = reverse(url_name, kwargs=kwargs)
                print(f"  ✓ {url_name:40} -> {url}")
                successful_urls += 1
                category_success += 1
            except NoReverseMatch as e:
                print(f"  ✗ {url_name:40} -> ERREUR: {e}")
                failed_urls.append((url_name, str(e)))
        
        print(f"  Total: {category_success}/{len(urls)} URLs OK")
    
    print("\n" + "="*80)
    print("RÉSUMÉ FINAL")
    print("="*80)
    print(f"\nTotal URLs testées: {total_urls}")
    print(f"URLs fonctionnelles: {successful_urls} ({successful_urls*100//total_urls}%)")
    print(f"URLs défaillantes: {len(failed_urls)}")
    
    if failed_urls:
        print("\n❌ URLs qui échouent:")
        for url_name, error in failed_urls:
            print(f"  - {url_name}")
    else:
        print("\n✅ TOUTES LES URLs FONCTIONNENT CORRECTEMENT!")
    
    print("\n" + "="*80)
    
    return len(failed_urls) == 0


if __name__ == '__main__':
    success = test_all_urls()
    exit(0 if success else 1)
