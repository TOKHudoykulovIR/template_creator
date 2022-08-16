from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from .models import Blank, BlankMeta, Furniture
from .forms import BlankForm, BlankMetaInlineFormset, FurnitureInlineFormset, FurnitureForm
from django.http import HttpResponse
from django.views.generic import View, CreateView
from .process import html_to_pdf
from django.urls import reverse
from django.contrib import messages


def home(request):
    context = {}
    return render(request, 'home.html', context)


#
# def add_blank(request):
#     submitted = False
#     ActionFormset = modelformset_factory(model=Action, form=ActionCreateForm, extra=2)
#     if request.method == 'POST':
#
#         form = BlankForm(request.POST)
#         # form2 = ActionCreateForm(request.POST)
#         formset = ActionFormset()
#         print(formset)
#
#         if form.is_valid() and formset.is_valid():
#             parent = form.save(commit=False)
#             parent.save()
#             # child = formset.save(commit=False)
#             # child.blank = parent
#             for f in formset:
#                 child = f.save(commit=False)
#                 child.blank = parent
#                 child.save()
#
#             return HttpResponseRedirect('/blank/add_blank?submitted=True')
#     else:
#         form = BlankCreateForm(request.POST)
#         # form2 = ActionCreateForm
#
#         ActionFormset = modelformset_factory(Action, form=ActionCreateForm, extra=2)
#         formset = ActionFormset(request.POST, queryset=Action.objects.none())
#
#     if 'submitted' in request.GET:
#         submitted = True
#
#     context = {
#         'form': form,
#         # 'form2': form2,
#         'formset': formset,
#         'submitted': submitted,
#     }
#     return render(request, "add_blank.html", context)


def blank_list(request):
    blanks = Blank.objects.all()
    context = {"blanks": blanks}

    return render(request, "blank_list.html", context)


def blank_detail(request, blank_id):
    blank = get_object_or_404(Blank, id=blank_id)
    context = {"blank": blank}
    return render(request, "blank_detail.html", context)


def delete_blank(request, blank_id):
    blank = get_object_or_404(Blank, id=blank_id)
    if request.user.is_superuser:
        blank.delete()
        messages.success(request, 'Blank successfully deleted')
        return redirect('blanks-list')
    else:
        messages.success(request, 'You are not rightful')
        return redirect('blanks-list')


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        print()
        print(args, kwargs)
        data = get_object_or_404(Blank, id=kwargs["blank_id"])
        print(data, data.event_manager)
        blank_meta = BlankMeta.objects.filter(blank=kwargs['blank_id'])
        furniture = Furniture.objects.filter(blank=kwargs['blank_id'])

        file = open('templates/tempr.html', "w")
        file.write(render_to_string('result.html', {
            'data': data,
            'meta': blank_meta,
            'furniture': furniture
        }))
        file.close()
        # Converting the HTML template into a PDF file a
        pdf = html_to_pdf('tempr.html')
        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


class BlankCreateView(CreateView):
    form_class = BlankForm
    template_name = 'add_blank.html'

    def get_context_data(self, **kwargs):
        context = super(BlankCreateView, self).get_context_data(**kwargs)
        context['blank_meta_formset'] = BlankMetaInlineFormset()
        context['furniture_formset'] = FurnitureInlineFormset(
            initial=[
                {"row_header": "t"},
                {"row_header": "tl"},
                {"row_header": "n"},
                {"row_header": "d"},
            ]
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        blank_meta_formset = BlankMetaInlineFormset(self.request.POST)
        furniture_formset = FurnitureInlineFormset(self.request.POST)

        if form.is_valid() and blank_meta_formset.is_valid() and furniture_formset.is_valid():
            return self.form_validd(form, blank_meta_formset, furniture_formset)
        else:
            return self.form_invalidd(form, blank_meta_formset, furniture_formset)

    def form_validd(self, form, blank_meta_formset, furniture_formset):
        self.object = form.save(commit=False)
        self.object.save()
        # saving ProductMeta Instances
        blank_metas = blank_meta_formset.save(commit=False)
        furniture = furniture_formset.save(commit=False)

        for meta in blank_metas:
            meta.blank = self.object
            meta.save()

        for fur in furniture:
            fur.blank = self.object
            fur.save()

        messages.success(self.request, 'Saved')
        return redirect(reverse("blanks-list"))

    def form_invalidd(self, form, blank_meta_formset, furniture_formset):
        messages.error(self.request, 'Something went wrong, check the format of fields')
        return self.render_to_response(
            self.get_context_data(
                form=form,
                blank_meta_formset=blank_meta_formset,
                furniture_formset=furniture_formset,
            )
        )


def blank_update(request, blank_id):
    blank = Blank.objects.get(id=blank_id)
    form = BlankForm(request.POST or None, instance=blank)

    FurnitureTableFormset = inlineformset_factory(
        Blank,
        Furniture,
        form=FurnitureForm,
        extra=4,
        max_num=4,
        can_delete=False
    )
    formset = FurnitureTableFormset(request.POST or None, instance=blank)

    if form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        return redirect('blanks-list')
    context = {
        'form': form,
        'blank': blank,
        "formset": formset
    }
    return render(request, 'blank_update_form.html', context)
